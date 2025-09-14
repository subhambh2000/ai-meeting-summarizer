import os.path
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File
from fastapi import Request
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from app.auth.routes import router, get_current_user
from app.auth.schemas import UserOut
from app.services.database import init_db
from app.services.db_service import save_meeting, get_all_meetings, get_meeting_by_id
from app.services.pdf_service import pdf_generator
from app.services.stt_service import transcribe_audio
from app.services.summary_service import summarize_text


@asynccontextmanager
async def lifespan(api_app: FastAPI):
    # Initialize the database when the application starts
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

# Directory to store uploaded files temporarily
UPLOAD_DIR = "uploads"
# Ensure the directory exists, creating it if necessary
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Directory to store generated PDF files
RESULTS_DIR = "results"
# Ensure the results directory exists, creating it if necessary
os.makedirs(RESULTS_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=RESULTS_DIR), name="static")


@app.get("/health")
def health_check():
    return {"status": "200"}


app.include_router(router)


@app.post("/process")
async def process_meeting(file: UploadFile = File(...), current_user: UserOut = Depends(get_current_user)):
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

    # Set pdf file path with versioning

    pdf_file_base_name = file.filename.removesuffix(".mp3")
    pdf_file_path = os.path.join(RESULTS_DIR, f"{pdf_file_base_name}_v1.pdf")
    version = 1
    while os.path.exists(pdf_file_path):
        version += 1
        pdf_file_path = os.path.join(RESULTS_DIR, f"{pdf_file_base_name}_v{version}.pdf")

    with open(file_path, "wb") as writer:
        writer.write(await file.read())

    transcript = transcribe_audio(file_path)

    if not transcript:
        return JSONResponse(
            content={"error": "Failed to transcribe audio."},
            status_code=500
        )

    summary = summarize_text(transcript=transcript)

    pdf_generator(pdf_file_path, transcript, summary)

    meeting_id = save_meeting(file.filename, transcript, summary, os.path.abspath(pdf_file_path), current_user.id)

    if meeting_id is None:
        return JSONResponse(
            content={"error": "Failed to save meeting to the database."},
            status_code=500
        )

    content = {"meeting_id": meeting_id, "message": "Meeting processed successfully"}

    return JSONResponse(content=content, status_code=200)


@app.get("/meetings")
async def list_meetings(current_user: UserOut = Depends(get_current_user)):
    meetings = get_all_meetings(current_user)
    if meetings is None:
        return JSONResponse(
            content={"error": "Failed to retrieve meetings."},
            status_code=500
        )

    return JSONResponse(content=meetings, status_code=200)


@app.get("/meeting/{id}")
async def get_meeting_details(id: int, request: Request):
    meeting = get_meeting_by_id(id)
    if meeting is None:
        return JSONResponse(
            content={"error": "Meeting not found."},
            status_code=404
        )

    pdf_name = os.path.basename(meeting[4])
    pdf_path = f"{request.base_url}static/{pdf_name}"

    result = {
        "id": meeting[0],
        "filename": meeting[1],
        "transcript": meeting[2],
        "summary": meeting[3],
        "created_at": meeting[5],
        "download_url": pdf_path
    }
    return JSONResponse(content=result, status_code=200)

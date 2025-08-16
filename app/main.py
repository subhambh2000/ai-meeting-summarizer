import os.path
import uuid

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

from app.pdf_service import pdf_generator
from app.stt_service import transcribe_audio
from app.summary_service import summarize_text

app = FastAPI()

# Directory to store uploaded files temporarily
UPLOAD_DIR = "uploads"
# Ensure the directory exists, creating it if necessary
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Directory to store generated PDF files
RESULTS_DIR = "results"
# Ensure the results directory exists, creating it if necessary
os.makedirs(RESULTS_DIR, exist_ok=True)


@app.get("/health")
def health_check():
    return {"status": "200"}


@app.post("/process")
async def process_meeting(file: UploadFile = File(...)):
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

    result = {
        "id": file_id,
        "file": file.filename,
        "transcript": transcript,
        "summary": summary,
        "pdf_url": f"{pdf_file_path}"
    }

    return JSONResponse(content=result, status_code=200)

# AI Meeting Summarizer

AI Meeting Summarizer is a robust Python-based tool designed to transcribe and summarize meeting audio using advanced AI
models. It generates accurate transcripts, concise summaries, and professional PDF reports, making it ideal for teams
and individuals seeking efficient meeting documentation.

## Features

- 🎤 **Audio Transcription:** Converts meeting audio files into accurate, timestamped text transcripts.
- 📝 **AI-Powered Summarization:** Produces concise, context-aware summaries of meetings.
- 📄 **PDF Report Generation:** Creates well-formatted PDF reports, including summaries and full transcript appendices.
- 🔒 **Authentication Support:** Secure access and usage with integrated authentication (if applicable).
- 📂 **Batch Processing:** Supports processing multiple audio files in one go.
- 🛠️ **Easy Integration:** Simple to integrate into existing workflows or automation pipelines.
- 🖥️ **User-Friendly CLI:** Intuitive command-line interface for quick operation.

## Requirements

- Python 3.7+
- [FastAPI](https://fastapi.tiangolo.com/) (for API server)
- [Groq](https://pypi.org/project/groq/) (AI model integration)
- [FPDF](https://pyfpdf.github.io/fpdf2/) (PDF report generation)
- [Pydantic](https://docs.pydantic.dev/) (data validation)
- [python-jose](https://python-jose.readthedocs.io/) and [passlib](https://passlib.readthedocs.io/) (authentication)
- [bcrypt](https://pypi.org/project/bcrypt/) or [argon2-cffi](https://pypi.org/project/argon2-cffi/) (password hashing)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/subhambh2000/ai-meeting-summarizer.git
   cd ai-meeting-summarizer
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

### 1. Start the API Server

Run the FastAPI application:

```sh
  uvicorn app.main:app --reload
```

### 2. Authentication

All main endpoints require authentication. Obtain a token using your authentication flow (see project docs or `/auth`
endpoints).

### 3. Process a Meeting Audio File

Send a POST request to `/process` with your audio file and authentication token:

```sh
  curl -X POST "http://localhost:8000/process" \
    -H "Authorization: Bearer <your_token>" \
    -F "file=@path/to/meeting.mp3"
```

- Returns: Meeting ID and success message.

### 4. List All Meetings

```sh
  curl -X GET "http://localhost:8000/meetings" \
    -H "Authorization: Bearer <your_token>"
```

- Returns: List of meetings for the authenticated user.

### 5. Get Meeting Details and Download PDF

```sh
  curl -X GET "http://localhost:8000/meeting/<meeting_id>"
```

- Returns: Meeting details, transcript, summary, and a direct PDF download URL.

## Environment Variables

Before running the application, set the following environment variables:

- `GROQ_API_KEY` – Your Groq API key
- `JWT_SECRET_KEY` – Secret key for JWT authentication
- `ACCESS_TOKEN_EXPIRE_MINUTES` – Token expiry time in minutes (default: 60)

You can set these in a `.env` file or directly in your environment.  
**Sample `.env` file:**

```env
GROQ_API_KEY=your_groq_api_key
JWT_SECRET_KEY=your_jwt_secret
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

**Note:** The application will not run without these variables set.

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements.

## License

This project is licensed under the MIT License.

## Contact

For questions or support, contact [subhambh2000](https://github.com/subhambh2000).

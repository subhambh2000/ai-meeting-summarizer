import os

from groq import Groq

ai_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def transcribe_audio(audio_file_path: str):
    with open(audio_file_path, "rb") as reader:
        transcription = ai_client.audio.transcriptions.create(
            file=reader,
            model="whisper-large-v3-turbo",
            response_format="verbose_json",
        )
    return transcription.text

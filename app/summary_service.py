import os
import re

from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def summarize_text(transcript: str):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[

                {
                    "role": "system",
                    "content": "You are a meeting assistant"
                },
                {
                    "role": "user",
                    "content": f"Summarize the following meeting transcript:\n\n{transcript}\n\nBullet summary and Action items"
                }
            ],
            temperature=0,
            max_completion_tokens=1024,
            top_p=1,
            stream=True
        )
        summary = "".join(chunk.choices[0].delta.content or "" for chunk in response)
        summary = re.sub(r"\n{2,}", "\n",
                         summary.replace("**", ""))  # Remove any Markdown formatting and extra newlines
        return summary.strip()

    except Exception as e:
        return f"Error summarizing text: {str(e)}"

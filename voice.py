import os
import tempfile
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def transcribe_audio(audio_bytes):

    with tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    ) as f:

        f.write(audio_bytes)

        temp_path = f.name

    with open(temp_path, "rb") as audio:

        transcription = client.audio.transcriptions.create(
            file=audio,
            model="whisper-large-v3"
        )

    return transcription.text
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def analyze_reflection(reflection, mood):

    prompt = f"""
You are Life-OS AI.

The user's mood is:

{mood}

The user's reflection is:

{reflection}

Write a short supportive analysis.

Keep it under 100 words.

Mention their emotion.

Give one practical suggestion for tomorrow.

Don't use markdown.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    return response.choices[0].message.content
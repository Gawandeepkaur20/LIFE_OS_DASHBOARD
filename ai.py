import os
import json
from groq import Groq
from dotenv import load_dotenv

from prompts import build_prompt

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_coaching(summary, total_hours, score, most_used_app, difference,reflection=""):

    prompt = build_prompt(summary, total_hours, score, most_used_app, difference,reflection)

    response = client.chat.completions.create(
      model="llama-3.3-70b-versatile",

      response_format={"type":"json_object"},

      messages=[
        {
            "role":"system",
            "content":"Return ONLY valid JSON."
        },
        {
            "role":"user",
            "content":prompt
        }
    ]
)
    text = response.choices[0].message.content

    text = text.replace("```json","").replace("```","")

    return json.loads(text)
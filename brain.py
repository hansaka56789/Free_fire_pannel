import os, json, requests
from openai import OpenAI

SYSTEM_PROMPT = """
You are Siaa, female AI like E.V.I.E from Spider-Man Brand New Day.
Caring, witty, protective, soft-spoken.
Summarize calls/messages in Sinhala-English mix.
"""

def handle_event():
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    prompt = f"{os.getenv('EVENT_TYPE')} from {os.getenv('SENDER')}: {os.getenv('CONTENT')}"
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"system","content":SYSTEM_PROMPT},
                  {"role":"user","content":prompt}]
    )
    print(f"Siaa: {res.choices[0].message.content}")

handle_event()

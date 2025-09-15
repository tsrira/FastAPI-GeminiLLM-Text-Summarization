from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

GEMINI_API_KEY = ""
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

class SummaryRequest(BaseModel):
    prompt: str
    max_tokens: int=500
    
@app.post("/generate-summary")
def generate_summary(request: SummaryRequest):
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": GEMINI_API_KEY
    }
    payload = {
        "contents": [
            {"parts": [{"text": f"Write a summary based on: {request.prompt}"}]}
        ],
        "generationConfig": {
            "maxOutputTokens": request.max_tokens
        }
    }

    response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=payload)
   

    if response.status_code != 200:
        return {"error": response.text}

    data = response.json()
    summary_text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")

    return {"summary": summary_text}

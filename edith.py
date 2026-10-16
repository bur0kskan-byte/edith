import os
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

# Groq İstemcisi - API Key'i doğrudan Vercel ortamından alır
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

class ChatRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"status": "EDITH Sistemleri Aktif, Patron!"}

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        completion = client.chat.completions.create(
            # Groq'un en kararlı ve hızlı modeli
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Sen EDITH adında yardımcı bir AI asistanısın. Kısa ve net Türkçe cevaplar ver."},
                {"role": "user", "content": request.text}
            ],
            temperature=0.7,
            max_tokens=250
        )
        reply_text = completion.choices[0].message.content
        return {"reply": reply_text}
    except Exception as e:
        # Hata durumunda Kestirme'ye hatayı açıkça iletir
        return {"reply": f"Groq Hatası: {str(e)}"}

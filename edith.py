import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq

app = FastAPI(title="EDITH Voice Backend")

# Groq API Client
# GROQ_API_KEY ortam değişkeninden okunur
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

class UserRequest(BaseModel):
    text: str

SYSTEM_PROMPT = (
    "Sen EDITH'sin. Kullanıcının mutlak patronusun. "
    "Her zaman 'Efendim Patron' veya 'Patron' diyerek konuş. "
    "Sadece Türkçe yanıt ver. Yıldız, kare gibi işaretler veya emoji KULLANMA. "
    "Yanıtların sesli okunacağı için kısa, net ve karizmatik olsun."
)

@app.post("/chat")
async def chat_with_edith(request: UserRequest):
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Metin boş olamaz.")

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request.text}
            ],
            temperature=0.7,
            max_tokens=250
        )
        
        reply = completion.choices[0].message.content
        return {"reply": reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health_check():
    return {"status": "EDITH Sistemleri Aktif, Patron!"}
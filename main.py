from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import whisper
import tempfile
import shutil
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # Das ist deine Laravel-Entwicklungsumgebung
    allow_credentials=True,
    allow_methods=["*"],  # Erlaubt alle Methoden (GET, POST, etc.)
    allow_headers=["*"],  # Erlaubt alle Header, inkl. Authorization und Content-Type
)

model = whisper.load_model("base")  # oder "small", "medium"

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...), language: str = Form("de")):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        result = model.transcribe(tmp_path, language=language)
        os.remove(tmp_path)

        return JSONResponse(content={"text": result["text"]})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
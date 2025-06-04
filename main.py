from fastapi import FastAPI, File, UploadFile
import whisper
import tempfile

app = FastAPI()

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    model = whisper.load_model("base")
    result = model.transcribe(tmp_path)

    return {"transcript": result["text"]}
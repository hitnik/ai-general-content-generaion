from fastapi import FastAPI, File, UploadFile
import whisper
import tempfile

app = FastAPI()
model = whisper.load_model("large")  # or "base", "small", etc.


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/v1/stt")
async def transcribe(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    result = model.transcribe(tmp_path)
    return {"text": result["text"]}


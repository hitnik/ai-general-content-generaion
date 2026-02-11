from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
import whisper
import tempfile
from TTS.api import TTS

app = FastAPI()
model = whisper.load_model("large")  # or "base", "small", etc.
MODEL_NAME = "tts_models/en/ljspeech/tacotron2-DDC"
tts = TTS(model_name=MODEL_NAME, progress_bar=False)


@app.post("/v1/stt")
async def speech_to_text(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    result = model.transcribe(tmp_path)
    return {"text": result["text"]}


@app.post("/v1/tts")
async def text_to_spech(text: str = Form(...), speaker: str = Form(None)):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
        wav_path = tmpfile.name
        if speaker and tts.speakers:
            tts.tts_to_file(text=text, speaker=speaker, file_path=wav_path)
        else:
            tts.tts_to_file(text=text, file_path=wav_path)

        # Return the WAV file
        response = FileResponse(wav_path, media_type="audio/wav", filename="speech.wav")
        # Optionally, schedule file cleanup after sending
        return response

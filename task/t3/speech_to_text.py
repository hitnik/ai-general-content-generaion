import sounddevice as sd
from scipy.io.wavfile import write
from pydub import AudioSegment
import tempfile
import os
import numpy as np
import aiohttp
import asyncio

fs = 16000  # Sample rate


def record_audio(output_file):
    print("Press Enter to start recording...")
    input()
    print("Recording... Press Enter to stop.")
    # Start recording
    recording = []

    def callback(indata, frames, time, status):
        recording.append(indata.copy())

    with sd.InputStream(samplerate=fs, channels=1, dtype="int16", callback=callback):
        input()  # Wait for Enter to stop

    print("Recording stopped.")

    # Concatenate all chunks
    audio_data = np.concatenate(recording, axis=0)

    # Save as WAV
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as wavfile:
        write(wavfile.name, fs, audio_data)
        wav_path = wavfile.name

    # Convert WAV to MP3
    audio = AudioSegment.from_wav(wav_path)
    audio.export(output_file, format="mp3")
    os.remove(wav_path)  # Clean up WAV file

    print(f"Saved MP3: {output_file}")


async def speech_to_text(voice_file, url):
    async with aiohttp.ClientSession() as session:
        with open(voice_file, "rb") as f:
            data = aiohttp.FormData()
            data.add_field("file", f, filename="audio.mp3", content_type="audio/mpeg")
            async with session.post(url, data=data) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    print("Transcription:", result.get("text"))
                else:
                    print("Error:", await resp.text())


if __name__ == "__main__":
    output_file = "output.mp3"
    record_audio(output_file)
    asyncio.run(speech_to_text(output_file, "http://127.0.0.1:8000/v1/stt"))

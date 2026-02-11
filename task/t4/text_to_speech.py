import asyncio
import aiohttp



async def text_to_speech(text: str, url: str, output_path: str = "output.wav") -> str:
    async with aiohttp.ClientSession() as session:

        data = aiohttp.FormData()
        data.add_field("text", text)
        async with session.post(url, data=data) as resp:
            if resp.status == 200:
                with open(output_path, "wb") as f:
                    f.write(await resp.read())
                    print(f"Audio saved to {output_path}")
            else:
                print(f"Error: {resp.status}")
                print(await resp.text())


if __name__ == "__main__":
    url = "http://localhost:8000/v1/tts"
    text = "easy fix to your bug is to add punctuation to the end. And classification errors of models are not counted as a bug. At least we don't. So I suggested moving it to discussions."
    asyncio.run(text_to_speech(text, url=url, output_path="tts_output.wav"))
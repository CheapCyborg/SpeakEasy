import os
from voicevox import Client

# Set the output directory path
output_directory = "./tmp" 

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

async def generate_waifu(speaker=1):
    async with Client() as client:
        with open("./tmp/translation.txt", "r", encoding="utf-8") as f:
            translation = f.read()
        audio_query = await client.create_audio_query(
            translation, speaker=speaker
        )
        with open(os.path.join(output_directory, "voice.wav"), "wb") as f:
            f.write(await audio_query.synthesis(speaker=speaker))
        
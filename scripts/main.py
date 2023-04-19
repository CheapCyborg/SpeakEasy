import os
import sys
import asyncio

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from select_device import select_input_device
from record_audio import record_audio
from transcribe import transcribe
from translate import translate_text
from generate_voice import generate_waifu

# Get the hotkey from the .env file

async def main():
    # Run the select_device.py script to prompt the user to choose an input device
    input_device = select_input_device()

    # Run the record_audio.py script to record audio using the chosen input device
    record_audio(input_device)

    # Get the transcription from the recorded audio
    transcription = transcribe()

    # Translate the transcription
    translated_text = translate_text(transcription)

    # Generate voice from the translated text
    await generate_waifu(translated_text)

asyncio.run(main())

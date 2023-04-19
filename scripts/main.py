import os
import sys
import asyncio

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from select_device import select_input_device, select_output_device
from record_audio import record_audio
from transcribe import transcribe
from translate import translate_text
from generate_voice import generate_waifu

async def main():
    # Run the select_device.py script to prompt the user to choose an input device
    input_device = select_input_device()

    # Run the record_audio.py script to record audio using the chosen input device
    record_audio(input_device)

    # Get the transcription from the recorded audio
    transcription = transcribe()

    # Translate the transcription
    translated_text = translate_text(transcription)

    # Prompt the user to ask if they would like to generate a waifu voice
    while True:
        user_input = input("Generate a waifu voice? (y/n): ")
        if user_input.lower() == 'y':
            # Select the output device
            output_device = select_output_device()
            # Generate voice from the translated text
            await generate_waifu(translated_text, output_device=output_device)
            break
        elif user_input.lower() == 'n':
            print("No anime girls for you, then! 😢")
            break
        else:
            print("Invalid input. Enter 'y' or 'n'")

asyncio.run(main())

import os
import sys
import keyboard
import asyncio

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from record_audio import record_audio
from transcribe import transcribe
from translate import translate_text
from generate_voice import generate_waifu

# main.py

# main.py
async def main(input_device, output_device, is_running, status_callback=None):
    while is_running():
        # Run the record_audio.py script to record audio using the chosen input device
        print("Starting record_audio")
        await record_audio(input_device, status_callback=status_callback)
        print("Finished record_audio")

        # Get the transcription from the recorded audio
        print("Starting transcribe")
        transcription = await transcribe()
        print("Finished transcribe")

        # Translate the transcription
        print("Starting translate_text")
        translated_text = await translate_text(transcription, status_callback=status_callback)
        print("Finished translate_text")

        # Generate voice from the translated text
        print("Starting generate_waifu")
        await generate_waifu(translated_text, output_device=output_device, status_callback=status_callback)
        print("Finished generate_waifu")

        # Check if the user wants to quit the application
        if keyboard.is_pressed('q'):
            print("Goodbye! 😊")
            break
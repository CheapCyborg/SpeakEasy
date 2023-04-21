import os
import sys
import keyboard
import asyncio
import faulthandler
   
faulthandler.enable()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from record_audio import record_audio
from transcribe import transcribe
from translate import translate_text
from generate_voice import generate_waifu
from gui import app_is_closing

#TODO: Handle errors in the main.py script and display them in the GUI instead of the console window

async def main(input_device, output_device, status_queue=None, cancel_event=None):
    while not (app_is_closing or (cancel_event and cancel_event.is_set())):
        # Run the record_audio.py script to record audio using the chosen input device
        print("Starting record_audio")
        await record_audio(input_device, status_queue=status_queue)
        print("Finished record_audio")

        # Get the transcription from the recorded audio
        print("Starting transcribe")
        transcription =  transcribe()
        print("Finished transcribe")

        # Translate the transcription
        print("Starting translate_text")
        translated_text =  translate_text(transcription, status_queue=status_queue)
        print("Finished translate_text")

        # Generate voice from the translated text
        print("Starting generate_waifu")
        await generate_waifu(translated_text, output_device=output_device, status_queue=status_queue)
        print("Finished generate_waifu")

        # Check if the user wants to quit the application
        if keyboard.is_pressed('q'):
            print("Goodbye! 😊")
            break

        # If cancel_event is set, break the loop
        if cancel_event and cancel_event.is_set():
            break

        # Add a short sleep before the next iteration to avoid blocking the event loop
        await asyncio.sleep(0.1)

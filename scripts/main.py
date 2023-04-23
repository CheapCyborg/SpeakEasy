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

async def main(input_device, output_device, deepl_api_key, status_queue=None, cancel_event=None):
    print ("main() called")
    while not (app_is_closing or (cancel_event and cancel_event.is_set())):
        print("Before record_audio(")
        await record_audio(input_device, status_queue=status_queue)
        print("After record_audio(")

        print("Before transcribe()")
        transcription =  transcribe()
        print("After transcribe()")

        print("Before translate_text()")
        translated_text =  translate_text(transcription, deepl_api_key, status_queue=status_queue)
        print("After translate_text()")

        print("Before generate_waifu()")
        await generate_waifu(translated_text, output_device=output_device, status_queue=status_queue)
        print("After generate_waifu()")

        # If cancel_event is set, break the loop
        if cancel_event and cancel_event.is_set():
            if status_queue:
                status_queue.put("Goodbye! 😊")
            break

        # Add a short sleep before the next iteration to avoid blocking the event loop
        await asyncio.sleep(0.1)

from gui import app_is_closing
from generate_voice import generate_waifu
from translate import translate_text
from transcribe import transcribe
from record_audio import record_audio
import os
import sys
import keyboard
import asyncio
import faulthandler

faulthandler.enable()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# TODO: Handle errors in the main.py script and display them in the GUI instead of the console window


def main(input_device, output_device, status_queue, cancel_event):
        
    while not app_is_closing:
        asyncio.run(record_audio(input_device, status_queue=status_queue))
        transcript = asyncio.run(transcribe(status_queue=status_queue))
        translation = asyncio.run(translate_text(transcript, status_queue=status_queue))
        asyncio.run(generate_waifu(translation, output_device=output_device, status_queue=status_queue))
    cancel_event.set()
    status_queue.put("Exiting main loop\n")
    return

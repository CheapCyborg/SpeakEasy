import os
import sys
import faulthandler
import asyncio

faulthandler.enable()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from record_audio import record_audio
from transcribe import transcribe
from translate import translate_text
from generate_voice import generate_waifu


output_directory = "./tmp" 

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

async def main(input_device, output_device, status_queue=None):
    try:
        successful_recording = await record_audio(input_device, status_queue=status_queue)
        if successful_recording:
            if status_queue:
                status_queue.put("Transcribing audio...\n")
            try:
                transcription = await transcribe(os.path.join(output_directory, "output.wav"))
                if status_queue:
                    status_queue.put("Original text: " + transcription + "\n")
            except FileNotFoundError:
                if status_queue:
                    status_queue.put("No transcription found\n")

            if status_queue:
                status_queue.put("Translating text...\n")
            translated_text = await translate_text(transcription, status_queue=status_queue)
            if status_queue:
                status_queue.put(f"Translated text: {translated_text}\n")

            if status_queue:
                status_queue.put("Generating voice...\n")
            await generate_waifu(translated_text, speaker=1, output_device=output_device, status_queue=status_queue)
            if status_queue:
                status_queue.put(f"Generated voice for: {translated_text}\n")

        else:
            if status_queue:
                status_queue.put("Recording was unsuccessful\n")

    except Exception as e:
        if status_queue:
            status_queue.put(f"Error in main loop: {str(e)}\n")
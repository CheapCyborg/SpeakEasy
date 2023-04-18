# main.py
import os
from select_device import select_input_device
from record_audio import record_audio
from dotenv import load_dotenv
from transcribe import transcribe

load_dotenv()

# Get the hotkey from the .env file
HOTKEY = os.getenv("HOTKEY")

# Run the select_device.py script to prompt the user to choose an input device
input_device = select_input_device()

# Run the record_audio.py script to record audio using the chosen input device
record_audio(input_device, HOTKEY)

# Get the transcription from the recorded audio
transcribe()
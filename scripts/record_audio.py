import os
import sounddevice as sd
import numpy as np
import wave
from pynput import keyboard
import time
import asyncio
from dotenv import load_dotenv

load_dotenv()

HOTKEY = os.getenv("HOTKEY")

# Set the output directory path
output_directory = "./tmp"

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

async def record_audio(input_device, status_queue=None):
    global is_recording
    # Initialize an empty list to store audio data
    audio_data = []
    is_recording = False
    
    # Define a callback function to record audio
    def callback(indata, frames, time, status):
        if is_recording:
            audio_data.append(indata.copy())

    # Set the recording parameters
    FORMAT = np.int16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    WAVE_OUTPUT_FILENAME = os.path.join(output_directory, "output.wav")

    # Define a function to handle key press events
    def on_press(key):
        if key == keyboard.KeyCode.from_char(HOTKEY):
            global is_recording
            is_recording = True
            if status_queue:
                status_queue.put(f"Recording started")

    # Define a function to handle key release events
    def on_release(key):
        if key == keyboard.KeyCode.from_char(HOTKEY):
            global is_recording
            is_recording = False
            if status_queue:
                status_queue.put(f"Recording stopped")
            return False  # Stop the listener

    with sd.InputStream(samplerate=RATE, channels=CHANNELS, dtype=FORMAT, blocksize=CHUNK, callback=callback, device=input_device):
        # Wait for the hotkey to be pressed and released
        if status_queue:
            status_queue.put(f"Press and hold the '{HOTKEY}' key to start recording")

        # Start a listener to detect key press and release events
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

        if status_queue:
            status_queue.put("Finished recording\n")

    # Concatenate the recorded audio chunks
    audio_data = np.vstack(audio_data)

    # Save the recorded audio to a WAV file
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(np.dtype(FORMAT).itemsize)
        wf.setframerate(RATE)
        wf.writeframes(audio_data.tobytes())

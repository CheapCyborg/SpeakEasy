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

output_directory = "./tmp"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
    

async def record_audio(input_device, status_queue=None):
    print("record_audio() called")
    global is_recording, recording_started

    is_recording = False
    recording_started = False
    
    def on_press(key):
        global is_recording, recording_started
        try:
            if key.char == HOTKEY:
                is_recording = True
                recording_started = True
        except AttributeError:
            pass
        
    def on_release(key):
        global is_recording
        try:
            if key.char == HOTKEY:
                is_recording = False
        except AttributeError:
            pass
        
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        while not is_recording:
            await asyncio.sleep(0.1)
        print("Recording started")
        if status_queue:
            status_queue.put("Recording started\n")
        frames = []
        with sd.InputStream(device=input_device, channels=2, callback=callback):
            while is_recording:
                await asyncio.sleep(0.1)
            print("Recording stopped")
            if status_queue:
                status_queue.put("Recording stopped\n")
            return frames
    
def callback(indata, frames, time, status):
    frames.append(indata.copy())
        

import os
import sounddevice as sd
import numpy as np
import wave
import keyboard
import time


# Set the output directory path
output_directory = "./tmp" 

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

def record_audio(input_device, hotkey):
    # Initialize an empty list to store audio data
    audio_data = []

    # Define a callback function to record audio
    def callback(indata, frames, time, status):
        if keyboard.is_pressed(hotkey):
            audio_data.append(indata.copy())

    # Set the recording parameters
    FORMAT = np.int16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    WAVE_OUTPUT_FILENAME = os.path.join(output_directory, "output.wav")

    # Create an input stream with the callback function
    with sd.InputStream(samplerate=RATE, channels=CHANNELS, dtype=FORMAT, blocksize=CHUNK, callback=callback, device=input_device):
        # Wait for the hotkey to be pressed
        print(f"Press and hold the '{hotkey}' key to start recording")
        keyboard.wait(hotkey)

        # Record audio while the hotkey is pressed
        print("Recording...")
        while keyboard.is_pressed(hotkey):
            time.sleep(0.1)
        print("Finished recording\n")

    # Concatenate the recorded audio chunks
    audio_data = np.vstack(audio_data)

    # Save the recorded audio to a WAV file
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(np.dtype(FORMAT).itemsize)
        wf.setframerate(RATE)
        wf.writeframes(audio_data.tobytes()) 
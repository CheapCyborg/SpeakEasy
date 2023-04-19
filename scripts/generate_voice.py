import os
from voicevox import Client
import sounddevice as sd
import io
import numpy as np
import wave

# Set the output directory path
output_directory = "./tmp" 

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
    
def play_audio(wav_bytes, output_device):
    wav_obj = wave.open(io.BytesIO(wav_bytes), 'rb')
    n_channels, sampwidth, framerate, n_frames, comptype, compname = wav_obj.getparams()
    frames = wav_obj.readframes(n_frames)
    
    # Convert bytes to int16 NumPy array
    audio_data = np.frombuffer(frames, dtype=np.int16)
    # Normalize the audio data to float32
    audio_data = audio_data.astype(np.float32) / (2 ** (8 * sampwidth - 1))

    with sd.OutputStream(device=output_device, samplerate=framerate, channels=n_channels) as stream:
        stream.write(audio_data)


async def generate_waifu(translation, speaker=1, output_device=None):
    async with Client() as client:
        audio_query = await client.create_audio_query(
            translation, speaker=speaker
        )
        wav_data = await audio_query.synthesis(speaker=speaker)
        with open(os.path.join(output_directory, "voice.wav"), "wb") as f:
            f.write(wav_data)
        
        if output_device is not None:
            play_audio(wav_data, output_device)

        
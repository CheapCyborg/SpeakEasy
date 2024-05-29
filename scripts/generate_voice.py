import os
from voicevox import Client
import sounddevice as sd
import io
import numpy as np
import wave
import httpx

output_directory = "./tmp"

if not os.path.exists(output_directory):
    os.makedirs(output_directory)


def play_audio(wav_bytes, output_device, status_queue=None):
    wav_obj = wave.open(io.BytesIO(wav_bytes), 'rb')
    n_channels, sampwidth, framerate, n_frames, comptype, compname = wav_obj.getparams()
    frames = wav_obj.readframes(n_frames)

    # Convert bytes to int16 NumPy array
    audio_data = np.frombuffer(frames, dtype=np.int16)
    # Normalize the audio data to float32
    audio_data = audio_data.astype(np.float32) / (2 ** (8 * sampwidth - 1))

    with sd.OutputStream(device=output_device, samplerate=framerate, channels=n_channels) as stream:
        stream.write(audio_data)

    if status_queue:
        status_queue.put("Finished playing audio\n")


async def generate_waifu(translation, speaker=1, output_device=None, status_queue=None):
    try:
        async with Client() as client:
            if status_queue:
                status_queue.put(f"Attempting to generate voice...")

            audio_query = await client.create_audio_query(
                translation, speaker=speaker
            )
            wav_data = await audio_query.synthesis(speaker=speaker)
            with open(os.path.join(output_directory, "voice.wav"), "wb") as f:
                f.write(wav_data)

            if output_device is None:
                output_device = sd.default.device[1]

            play_audio(wav_data, output_device, status_queue=status_queue)

    except httpx.HTTPError as e:
        if status_queue:
            status_queue.put(
                f"httpx error: {e} (Probably didn't start VoiceVox Engine)\n")

import openai
import os
import asyncio

# Set the output directory path
output_directory = "./tmp" 

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

async def transcribe(audio_file_path):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _transcribe_blocking, audio_file_path)

def _transcribe_blocking(audio_file_path):
    try:
        with open(audio_file_path, "rb") as audio_file:
            # Check if the audio file exists
            if not os.path.isfile(audio_file.name):
                raise FileNotFoundError("Audio file not found")

            transcript = openai.Audio.transcribe("whisper-1", audio_file)

        # Write transcript to file
        transcript_text = transcript.text
        transcript_file_path = os.path.join(output_directory, "transcript.txt")
        with open(transcript_file_path, "w") as f:
            f.write(transcript_text)
        print(f"Transcription saved to {transcript_file_path}")
        return transcript.text
    except FileNotFoundError:
        print("Error: Audio file not found")
    except Exception as e:
        print(f"Error transcribing audio: {str(e)}")

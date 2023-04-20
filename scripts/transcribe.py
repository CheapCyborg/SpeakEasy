import openai
import os

# Set the output directory path
output_directory = "./tmp" 

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

async def transcribe():
    audio_file= open("./tmp/output.wav", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    # Write transcript to file
    transcript_text = transcript.text
    with open(os.path.join(output_directory, "transcript.txt"), "w") as f:
        f.write(transcript_text)
    print(f"Transcript saved to {os.path.join(output_directory, 'transcript.txt')}\n")
    return transcript.text

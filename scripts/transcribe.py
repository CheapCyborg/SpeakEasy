import openai
import os

# Path to save txt from transcription
output_directory = "./tmp"

def transcribe():
    audio_file= open("./tmp/output.wav", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    # Write transcript to file
    transcript_text = transcript.text
    with open(os.path.join(output_directory, "transcript.txt"), "w") as f:
        f.write(transcript_text)
    print(f"Transcript saved to {os.path.join(output_directory, 'transcript.txt')}")
    return transcript

import openai
import os

# Set the output directory path
output_directory = "./tmp" 

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

def transcribe(status_queue=None):
    # Set the output directory path
    output_directory = "./tmp"

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    try:
        audio_file = open("./tmp/output.wav", "rb")
    except FileNotFoundError as e:
        if status_queue:
            status_queue.put(f"Error: {e}")
        return None

    try:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    except Exception as e:
        if status_queue:
            status_queue.put(f"Error in transcription: {e}")
        return None

    transcript_text = transcript.text

    try:
        with open(os.path.join(output_directory, "transcript.txt"), "w") as f:
            f.write(transcript_text)
        if status_queue:
            status_queue.put(f"Transcript saved to {os.path.join(output_directory, 'transcript.txt')}\n")
    except IOError as e:
        if status_queue:
            status_queue.put(f"Error saving transcript: {e}")
        return None

    return transcript.text


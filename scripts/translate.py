import os
import deepl as dl
from dotenv import load_dotenv

load_dotenv()

auth_key = os.getenv("DEEPL_API_KEY")
translator = dl.Translator(auth_key)

# Set the output directory path
output_directory = "./tmp" 

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

def translate_text(lang="JA"):
    while True:
        user_input = input("Translate the transcription? (y/n): ")
        if user_input.lower() == 'y':
            # Get the transcription from the recorded audio
            with open("/tmp/transcript.txt", "r") as f:
                transcription = f.read()

            # Translate the transcription
            translation = translator.translate_text(transcription, target_lang=lang)

            # Write the translation to a text file
            with open(os.path.join(output_directory, "translation.txt"), "w", encoding='utf-8') as f:
                f.write(translation.text)

            print(f"\nOriginal: {transcription}")
            print(f"Translation: {translation.text}")
            break
    return translation.text

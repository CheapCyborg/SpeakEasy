import os
import deepl as dl
from dotenv import load_dotenv

load_dotenv()

auth_key = os.getenv("DEEPL_API_KEY")

# Set the output directory path
output_directory = "./tmp"

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

def translate_text(transcription, target_lang="JA", status_queue=None):
    translator = dl.Translator(auth_key)
    output_directory = "./tmp"

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    try:
        # Translate the text
        translation = translator.translate_text(transcription, target_lang="JA").text
    except Exception as e:
        if status_queue:
            status_queue.put(f"Error translating text: {e}")
        return None
    
    # Check if the translation is empty or if its an array
    if not translation or isinstance(translation, list):
        if status_queue:
            status_queue.put(f"Empty translation: {translation}")
        return None        

    try:
        # Write the translation to a text file
        with open(os.path.join(output_directory, "translation.txt"), "w", encoding='utf-8') as f:
            f.write(translation)
    except IOError as e:
        if status_queue:
            status_queue.put(f"Error saving translation: {e}")
        return None

    if status_queue:
        status_queue.put(f"Original: {transcription}\nTranslation: {translation}\n")

    return translation


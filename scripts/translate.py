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

def translate_text(transcription, deepl_api_key, target_lang="JA", status_queue=None):
    translator = dl.Translator(deepl_api_key)
    output_directory = "./tmp"

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    try:
        # Translate the transcription
        translations = translator.translate_text(transcription, target_lang=target_lang)
    except Exception as e:
        if status_queue:
            status_queue.put(f"Error in translation: {e}")
        return None

    # Check if translations is a list or TextResult object
    translation = translations[0].text if isinstance(translations, list) else translations.text

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


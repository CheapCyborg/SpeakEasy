import os
import deepl as dl
from dotenv import load_dotenv
import asyncio

load_dotenv()

auth_key = os.getenv("DEEPL_API_KEY")
translator = dl.Translator(auth_key)

# Set the output directory path
output_directory = "./tmp"

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

async def translate_text(transcription, target_lang="JA", status_queue=None):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _translate_blocking, transcription, target_lang, status_queue)


def _translate_blocking(transcription, target_lang="JA", status_queue=None):
    try:
        # Translate the transcription
        translations = translator.translate_text(transcription, target_lang=target_lang)

        # Check if translations is a list or TextResult object
        translation = translations[0].text if isinstance(translations, list) else translations.text

        # Write the translation to a text file
        with open(os.path.join(output_directory, "translation.txt"), "w", encoding='utf-8') as f:
            f.write(translation)

        return translation
    except dl.TranslatorError as e:
        if status_queue:
            status_queue.put(f"Error translating text: {str(e)}\n")

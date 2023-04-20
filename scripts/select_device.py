import sounddevice as sd
from dotenv import load_dotenv

load_dotenv()

# Get the list of audio devices
devices = sd.query_devices()
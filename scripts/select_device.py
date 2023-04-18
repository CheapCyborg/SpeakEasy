import sounddevice as sd
from dotenv import load_dotenv

load_dotenv()

# Get the list of audio devices
devices = sd.query_devices()
print("Audio devices:")

# Print input devices with their index and name
for i, device in enumerate(devices):
    if device['max_input_channels'] > 0:
        print(f"{i}: {device['name']}")

# Get the default input device name and number
default_input = sd.default.device[0]
default_input_name = devices[default_input]['name']

# Global variable to store the selected input device
input_device = None

# Prompt the user to select an input device or exit and use the default on press of 'y' or 'n'
def select_input_device():
    global input_device
    while True:
        user_input = input(
            f"\nUse default input device '({default_input}) {default_input_name}'? (y/n): ")
        if user_input.lower() == 'y':
            input_device = default_input
            break
        elif user_input.lower() == 'n':
            input_device = int(input("Enter the number of the input device you want to use: "))
            if input_device in range(len(devices)) and devices[input_device]['max_input_channels'] > 0:
                break
            else:
                print("Invalid input device number. Please enter a valid input device number.")
        else:
            print("Invalid input. Enter 'y' or 'n'")

    print(f"\nSelected input device: ({input_device}) {devices[input_device]['name']}\n\n")
    return input_device
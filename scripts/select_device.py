import sounddevice as sd
from dotenv import load_dotenv

load_dotenv()

# Get the list of audio devices
devices = sd.query_devices()

def print_output_devices():
    print("Audio devices:")
    # Print output devices with their index and name
    for i, device in enumerate(devices):
        if device['max_output_channels'] > 0:
            print(f"{i}: {device['name']}")


def valid_output_device(device_number):
    return device_number in range(len(devices)) and devices[device_number]['max_output_channels'] > 0


def select_output_device():
    print_output_devices()

    # Get the default output device name and number
    default_output = sd.default.device[1]
    default_output_name = devices[default_output]['name']

    while True:
        user_input = input(
            f"\nUse default output device '({default_output}) {default_output_name}'? (y/n): ")
        if user_input.lower() == 'y':
            return default_output
        elif user_input.lower() == 'n':
            output_device = int(input("Enter the number of the output device you want to use: "))
            if valid_output_device(output_device):
                print(f"Selected output device: ({output_device}) {devices[output_device]['name']}\n\n")
                return output_device
            else:
                print("Invalid output device number. Please enter a valid output device number.")
        else:
            print("Invalid input. Enter 'y' or 'n'")

def print_input_devices():
    print("Audio devices:")
    # Print input devices with their index and name
    for i, device in enumerate(devices):
        if device['max_input_channels'] > 0:
            print(f"{i}: {device['name']}")


def valid_input_device(device_number):
    return device_number in range(len(devices)) and devices[device_number]['max_input_channels'] > 0


def select_input_device():
    print_input_devices()

    # Get the default input device name and number
    default_input = sd.default.device[0]
    default_input_name = devices[default_input]['name']

    while True:
        user_input = input(
            f"\nUse default input device '({default_input}) {default_input_name}'? (y/n): ")
        if user_input.lower() == 'y':
            return default_input
        elif user_input.lower() == 'n':
            input_device = int(input("Enter the number of the input device you want to use: "))
            if valid_input_device(input_device):
                print(f"Selected input device: ({input_device}) {devices[input_device]['name']}\n\n")
                return input_device
            else:
                print("Invalid input device number. Please enter a valid input device number.")
        else:
            print("Invalid input. Enter 'y' or 'n'")

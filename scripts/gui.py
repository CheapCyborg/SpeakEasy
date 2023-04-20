import sys
import main
import asyncio
import sounddevice as sd

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QPlainTextEdit
from select_device import devices

app_is_closing = False

def populate_devices_dropdown(dropdown, device_type):
    default_device = sd.default.device[0] if device_type == "input" else sd.default.device[1]

    for i, device in enumerate(devices):
        if (device_type == "input" and device['max_input_channels'] > 0) or (device_type == "output" and device['max_output_channels'] > 0):
            device_name = f"{i}: {device['name']}"
            if i == default_device:
                device_name += " (Default)"
            dropdown.addItem(device_name, i)

    # Set the current index of the dropdown to the default device
    dropdown.setCurrentIndex(dropdown.findData(default_device))
    
async def run_app_async(input_device, output_device, app_is_closing):
    await main.main(input_device, output_device, app_is_closing, update_status)

from threading import Thread

def run_app():
    input_device = input_dropdown.currentData()
    output_device = output_dropdown.currentData()

    # Run the main function asynchronously in a separate thread
    thread = Thread(target=asyncio.run, args=(run_app_async(input_device, output_device, lambda: not app_is_closing),))
    thread.start()

    # Change the button text to "Cancel" and disable the input and output dropdowns
    start_button.setText("Cancel")
    input_dropdown.setEnabled(False)
    output_dropdown.setEnabled(False)
    reset_button.setEnabled(False)

def cancel_app():
    global app_is_closing
    app_is_closing = True

    # Reset the button text and enable the input and output dropdowns
    start_button.setText("Start")
    input_dropdown.setEnabled(True)
    output_dropdown.setEnabled(True)
    reset_button.setEnabled(True)

def update_status(status):
    output_text.appendPlainText(status)

def reset_to_default():
    input_dropdown.setCurrentIndex(input_dropdown.findData(sd.default.device[0]))
    output_dropdown.setCurrentIndex(output_dropdown.findData(sd.default.device[1]))

def run_gui():
    global input_dropdown, output_dropdown, output_text, start_button, reset_button, window, app_is_closing

    app = QApplication(sys.argv)

    window = QWidget()
    layout = QVBoxLayout()

    input_label = QLabel("Select input device:")
    layout.addWidget(input_label)

    input_dropdown = QComboBox()
    input_dropdown.setSizeAdjustPolicy(QComboBox.AdjustToContents)
    populate_devices_dropdown(input_dropdown, "input")
    layout.addWidget(input_dropdown)

    output_label = QLabel("Select output device:")
    layout.addWidget(output_label)

    output_dropdown = QComboBox()
    output_dropdown.setSizeAdjustPolicy(QComboBox.AdjustToContents)
    populate_devices_dropdown(output_dropdown, "output")
    layout.addWidget(output_dropdown)

    reset_button = QPushButton("Reset to Default")
    reset_button.clicked.connect(reset_to_default)
    layout.addWidget(reset_button)

    start_button = QPushButton("Start")
    start_button.clicked.connect(lambda: cancel_app() if start_button.text() == "Cancel" else run_app())
    layout.addWidget(start_button)

    output_label = QLabel("Output:")
    layout.addWidget(output_label)

    output_text = QPlainTextEdit()
    output_text.setReadOnly(True)
    layout.addWidget(output_text)

    window.setLayout(layout)
    window.show()

    app_is_closing = False
    sys.exit(app.exec())

if __name__ == "__main__":
    run_gui()
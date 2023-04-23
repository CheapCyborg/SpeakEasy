import sys
import main
import asyncio
import sounddevice as sd

from PySide6.QtCore import QObject, Signal, QRunnable, QThreadPool
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QPlainTextEdit, QLineEdit
from select_device import devices
from queue import Queue
from threading import Thread
from asyncio import Event

class AsyncRunner(QRunnable):
    def __init__(self, func, *args):
        super().__init__()
        self.func = func
        self.args = args

    def run(self):
        asyncio.run(self.func(*self.args))

class StatusEmitter(QObject):
    status_received = Signal(str)

app_is_closing = False
status_queue = Queue()
cancel_event = Event()
status_emitter = StatusEmitter()

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

async def run_app_async(input_device, output_device, deepl_api_key,cancel_event):
    print("run_app_async() called")
    await main.main(input_device, output_device, deepl_api_key, status_queue=status_queue, cancel_event=cancel_event)


def run_app():
    print("run_app() called")
    input_device = input_dropdown.currentData()
    output_device = output_dropdown.currentData()
    deepl_api_key = deepl_api_key_input.text()

    try:
        # Run the main function asynchronously in a separate thread
        runner = AsyncRunner(run_app_async, input_device, output_device, deepl_api_key, cancel_event)
        QThreadPool.globalInstance().start(runner)
    except Exception as e:
        status_queue.put(f"Error starting the application: {e}")
        return

    # Change the button text to "Cancel" and disable the input and output dropdowns
    start_button.setText("Cancel")
    input_dropdown.setEnabled(False)
    output_dropdown.setEnabled(False)
    reset_button.setEnabled(False)

def cancel_app():
    global app_is_closing
    app_is_closing = True
    cancel_event.set()

    # Reset the button text and enable the input and output dropdowns
    start_button.setText("Start")
    input_dropdown.setEnabled(True)
    output_dropdown.setEnabled(True)
    reset_button.setEnabled(True)

def update_status():
    global app_is_closing
    while not app_is_closing:
        try:
            status = status_queue.get()
            status_emitter.status_received.emit(status)
        except Exception as e:
            status_queue.put(f"Error updating status: {e}")
            return

def reset_to_default():
    input_dropdown.setCurrentIndex(input_dropdown.findData(sd.default.device[0]))
    output_dropdown.setCurrentIndex(output_dropdown.findData(sd.default.device[1]))

def on_status_received(status):
    output_text.appendPlainText(status)

def run_gui():
    global input_dropdown, output_dropdown, output_text, start_button, reset_button, window, app_is_closing, deepl_api_key_input

    try:
        app = QApplication(sys.argv)
    except Exception as e:
        print(f"Error initializing the application: {e}")
        return

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

    deepl_api_key_label = QLabel("DeepL API Key:")
    layout.addWidget(deepl_api_key_label)
    deepl_api_key_input = QLineEdit()
    layout.addWidget(deepl_api_key_input)

    #disable the start button until the user enters an API key for DeepL
    start_button = QPushButton("Start")
    start_button.clicked.connect(lambda: cancel_app() if start_button.text() == "Cancel" else run_app())
    start_button.setEnabled(False)
    layout.addWidget(start_button)

    output_label = QLabel("Output:")
    layout.addWidget(output_label)
    output_text = QPlainTextEdit()
    output_text.setReadOnly(True)
    layout.addWidget(output_text)

    window.setLayout(layout)
    window.show()

    def check_api_key():
        if deepl_api_key_input.text() != "":
            start_button.setEnabled(True)
        else:
            start_button.setEnabled(False)

    deepl_api_key_input.textChanged.connect(check_api_key)

    app_is_closing = False

    status_emitter.status_received.connect(on_status_received)
    status_thread = Thread(target=update_status)
    status_thread.start()

    try:
        sys.exit(app.exec())
    except Exception as e:
        print(f"Error running the application: {e}")
        return

if __name__ == "__main__":
    run_gui()
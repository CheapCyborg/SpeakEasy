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

class StatusEmitter(QObject):
    status_received = Signal(str)
    
    def __init__(self):
        super().__init__()
        
    def emit_status(self, status):
        self.status_received.emit(status)
        
    def __del__(self):
        self.status_received.disconnect()
        
class MainTask(QRunnable):
    def __init__(self, input_device, output_device, status_queue, cancel_event):
        super().__init__()
        self.input_device = input_device
        self.output_device = output_device
        self.status_queue = status_queue
        self.cancel_event = cancel_event
        
    def run(self):
        asyncio.run(main.main(self.input_device, self.output_device, self.status_queue, self.cancel_event))

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


def run_app():
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()

    input_device_label = QLabel("Input Device:")
    input_device_dropdown = QComboBox()
    populate_devices_dropdown(input_device_dropdown, "input")

    output_device_label = QLabel("Output Device:")
    output_device_dropdown = QComboBox()
    populate_devices_dropdown(output_device_dropdown, "output")


    status_text = QPlainTextEdit()
    status_text.setReadOnly(True)

    start_button = QPushButton("Start")
    stop_button = QPushButton("Stop")

    layout.addWidget(input_device_label)
    layout.addWidget(input_device_dropdown)
    layout.addWidget(output_device_label)
    layout.addWidget(output_device_dropdown)
    layout.addWidget(status_text)
    layout.addWidget(start_button)
    layout.addWidget(stop_button)

    window.setLayout(layout)
    window.show()

    def start():
        status_queue.queue.clear()
        cancel_event.clear()
        status_emitter.status_received.connect(status_text.appendPlainText)

        input_device = input_device_dropdown.currentData()
        output_device = output_device_dropdown.currentData()

        thread = Thread(target=main.main, args=(input_device, output_device, status_queue, cancel_event))
        thread.start()

        while not status_queue.empty():
            status = status_queue.get()
            status_emitter.status_received.emit(status)

    def stop():
        cancel_event.set()

    start_button.clicked.connect(start)
    stop_button.clicked.connect(stop)

    sys.exit(app.exec())


if __name__ == "__main__":
    run_app()

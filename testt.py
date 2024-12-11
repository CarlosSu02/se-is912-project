import sys
import asyncio
from qasync import QEventLoop, asyncSlot
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from anthropic import AsyncAnthropic

API_KEY_CLAUDE = "your_api_key_here"  # Replace with your actual API key


def get_client():
    return AsyncAnthropic(api_key=API_KEY_CLAUDE)


async def text_claude(prompt, text):
    await asyncio.sleep(5)
    return '???'


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Async Anthropic Example")
        self.setLayout(QVBoxLayout())

        self.label = QLabel("Click the button to get a response...")
        self.layout().addWidget(self.label)

        self.button = QPushButton("Get Response")
        self.button.clicked.connect(self.on_button_click)
        self.layout().addWidget(self.button)

    @asyncSlot()
    async def on_button_click(self):
        prompt = "Explain the benefits of asynchronous programming."
        text = "What is async programming?"

        self.label.setText("Fetching response...")

        response = await text_claude(prompt, text)

        self.label.setText(f"Response:\n{response}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    main_window = MainWindow()
    main_window.show()

    with loop:
        loop.run_forever()
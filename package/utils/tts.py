import pyttsx3
import time
from PyQt6.QtCore import QThread, pyqtSignal
from package.ui.toast_manager import toasts

"""
engine = pyttsx3.init()


def tts(text="Hola, esta es una prueba de pyttsx3."):
    try:
        engine.say(text)
        engine.runAndWait()

        if engine._inLoop:
            engine.endLoop()

    except Exception as e:
        print(f"Error: {e}")
        toasts().error(e)


def tts_stop():
    try:
        engine.stop()

    except Exception as e:
        print(f"Error: { e }")

        toasts().error(e)
"""


class TTSThread(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, text):
        super().__init__()
        self.text = text
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty("voices")
        # for voice in voices:
        #     print(
        #         f"Voice ID: {voice.id} - Name: {voice.name} - Lang: {voice.languages}"
        #     )

        self.engine.setProperty("voice", voices[2].id)

        self._stop_req = False

    def run(self):
        try:
            if self.engine is None:
                return

            self.engine.connect("started-word", self.check_stop)
            self.engine.say(self.text)
            self.engine.runAndWait()

            if self.engine._inLoop:
                self.engine.endLoop()

        except RuntimeError as re:
            self.error.emit(str("Ya se encuentra en ejecución una ventana."))

        except Exception as e:
            self.error.emit(str(e))

        finally:
            self.cleanup()
            self.finished.emit()

    def stop(self):
        self._stop_req = True

        try:
            if self.engine is None:
                return

            self.engine.stop()

        except Exception as e:
            self.error.emit(str(e))

    def check_stop(self, *args):
        if self._stop_req and self.engine is not None:
            self.engine.stop()

    def cleanup(self):
        # Libera el motor para evitar problemas al instanciar de nuevo
        try:
            del self.engine
            self.engine = None
        except Exception as e:
            self.error.emit(str(e))


def text_to_file_audio(content, output_file):
    try:
        engine = pyttsx3.init()

        engine.setProperty("voice", engine.getProperty("voices")[2].id)

        engine.save_to_file(content, output_file)
        engine.runAndWait()

        engine.stop()

    except Exception as e:
        print(f"Error: { e }")

        toasts().error(e)

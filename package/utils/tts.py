import pyttsx3
from PyQt6.QtCore import QThread, pyqtSignal
from package.ui.dialogs.toast_manager import toasts

'''
class TTSThread(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, text=None):
        super().__init__()
        self.text = text
        self.engine = pyttsx3.init()

        voices = self.engine.getProperty("voices")
        rate = self.engine.getProperty("rate")

        # for voice in voices:
        #     print(
        #         f"Voice ID: {voice.id} - Name: {voice.name} - Lang: {voice.languages}"
        #     )

        voice = voices[2].id if len(voices) > 2 else voices[1].id

        self.engine.setProperty("voice", voice)
        self.engine.setProperty("rate", rate - 20)

        self._stop_req = False

    def run(self):
        try:
            if self.engine is None:
                return

            print("tts:", self.text)
            if self.text is None:
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

'''


class TTSThread(
    QThread):  # Hereda de QThread, para gestionar un hilo independiente, evita que la el programa se congele
    finished = pyqtSignal()  # Señal de finalización
    error = pyqtSignal(str)  # Señal de error
    stop_requested = pyqtSignal()  # Señal para detener el TTS

    def __init__(self, text=None):
        super().__init__()

        self.text = text  # Texto a decir
        self.engine = None  # Variable de inicialización del motor
        self.stop_req = False  # Variable de control para detener el TTS
        self.stop_requested.connect(self.stop)  # Conectar la señal stop_requested al método stop

        # Inicialización del motor TTS
        self._initialize_engine()

    def _initialize_engine(self):
        """Inicializa el motor TTS (Pyttsx3)"""
        self.engine = pyttsx3.init()

        voices = self.engine.getProperty("voices")  # Voces disponibles en la computadora
        rate = self.engine.getProperty("rate")

        voice = voices[2].id if len(voices) > 2 else voices[1].id

        self.engine.setProperty("voice", voice)
        self.engine.setProperty("rate", rate - 20)

    def run(self):
        """Método que ejecuta el motor TTS"""
        try:
            if self.engine is None:
                print("Error: el motor TTS no se ha inicializado correctamente.")
                return

            # Verificar si el texto se ha asignado correctamente
            if not self.text:
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
        """Método para detener el TTS"""
        self.stop_req = True
        try:
            if self.engine is None:
                return
            self.engine.stop()
        except Exception as e:
            self.error.emit(str(e))

    def check_stop(self, *args):
        """Verifica si se debe detener el TTS"""
        if self.stop_req and self.engine is not None:
            self.engine.stop()

    def cleanup(self):
        """Libera recursos del motor TTS"""
        try:
            if self.engine:
                self.engine.stop()
            # del self.engine
            self.engine = None
        except Exception as e:
            self.error.emit(str(e))

    def restart_engine(self):
        """Reinicia el motor TTS para la próxima palabra"""
        self.cleanup()
        self._initialize_engine()


def text_to_file_audio(content, output_file):
    try:
        engine = pyttsx3.init()

        voices = engine.getProperty("voices")
        rate = engine.getProperty("rate")

        voice = voices[2].id if len(voices) > 2 else voices[1].id

        engine.setProperty("voice", voice)
        engine.setProperty("rate", rate - 20)

        engine.save_to_file(content, output_file)
        engine.runAndWait()

        engine.stop()

    except Exception as e:
        print(f"Error: {e}")

        toasts().error(e)
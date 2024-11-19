import pyttsx3
from package.ui.toast_manager import toasts


def tts():
    try:
        engine = pyttsx3.init()

        engine.say("Hola, esta es una prueba de pyttsx3.")
        engine.runAndWait()

        if engine._inLoop:
            engine.endLoop()

    except Exception as e:
        print(f"Error: {e}")
        toasts().error(e)

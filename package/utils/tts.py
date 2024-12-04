import pyttsx3
from package.ui.toast_manager import toasts

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

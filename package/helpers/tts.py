import pyttsx3

from pyqttoast import Toast, ToastPreset

from package.ui.toast_manager import toasts


# import time


def tts():
    try:
        raise Exception("?")

        engine = pyttsx3.init()
        # pyttsx3.speak("hi!")

        # print(engine._inLoop)

        # if engine._inLoop:
        #     time.sleep(2)

        engine.say("Hola, esta es una prueba de pyttsx3.")
        engine.runAndWait()

        if engine._inLoop:
            engine.endLoop()

    except Exception as e:
        print(f"Error: {e}")
        # toast = Toast()
        # toast.setDuration(5000)  # Hide after 5 seconds
        # toast.setTitle("Success! Confirmation email sent.")
        # toast.setText("Check your email to complete signup.")
        # toast.applyPreset(ToastPreset.SUCCESS)  # Apply style preset
        # toast.show()

        # Toasts(content=str(e)).error()

        # toast_error(e)
        # toasts.error(e)
        toasts().error(e)

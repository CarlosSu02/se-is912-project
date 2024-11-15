import pyttsx3

# import time


def tts():
    try:
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

import os
import pygame
from gtts import gTTS
import streamlit as st
import speech_recognition as sr
from googletrans import LANGUAGES, Translator

# Initialize global variables
isTranslateOn = False
translator = Translator()
pygame.mixer.init()

# Create a mapping between language names and language codes
language_mapping = {name: code for code, name in LANGUAGES.items()}

def get_language_code(language_name):
    return language_mapping.get(language_name, language_name)

def translator_function(spoken_text, from_language, to_language):
    return translator.translate(spoken_text, src=from_language, dest=to_language)

def text_to_voice(text_data, to_language):
    myobj = gTTS(text=text_data, lang=to_language, slow=False)
    myobj.save("cache_file.mp3")
    audio = pygame.mixer.Sound("cache_file.mp3")
    audio.play()
    os.remove("cache_file.mp3")

def main_process(output_placeholder, from_language, to_language):
    global isTranslateOn

    while isTranslateOn:
        rec = sr.Recognizer()
        with sr.Microphone() as source:
            output_placeholder.text("Listening...")
            rec.pause_threshold = 1
            audio = rec.listen(source, phrase_time_limit=10)

        try:
            output_placeholder.text("Processing...")
            spoken_text = rec.recognize_google(audio, language=from_language)

            output_placeholder.text("Translating...")
            translated_text = translator_function(spoken_text, from_language, to_language)

            text_to_voice(translated_text.text, to_language)

        except Exception as e:
            print(e)

def main():
    global isTranslateOn

    st.title("Language Translator with Speech Recognition")

    # Dropdowns for selecting languages
    from_language_name = st.selectbox("Select Source Language:", list(LANGUAGES.values()))
    to_language_name = st.selectbox("Select Target Language:", list(LANGUAGES.values()))

    # Convert language names to language codes
    from_language = get_language_code(from_language_name)
    to_language = get_language_code(to_language_name)

    # Button to trigger translation
    start_button = st.button("Start")
    stop_button = st.button("Stop")

    output_placeholder = st.empty()  # Placeholder for output messages

    # Check if "Start" button is clicked
    if start_button and not isTranslateOn:
        isTranslateOn = True
        output_placeholder.text("Translation started...")
        main_process(output_placeholder, from_language, to_language)

    # Check if "Stop" button is clicked
    if stop_button and isTranslateOn:
        isTranslateOn = False
        output_placeholder.text("Translation stopped.")

if __name__ == "__main__":
    main()

import speech_recognition as sr
from gtts import gTTS
from transformers import pipeline
from sty import fg
import time
import keyboard
import pygame
import io
import logging
logging.getLogger("transformers").setLevel(logging.ERROR)

#################################################
# This code will work perfectly for:
#################################################
# Qwen/Qwen2-1.5B
# microsoft/phi-2
# TinyLlama/TinyLlama-1.1B-Chat-v1.0
#################################################

# initializing tools
print(fg.blue + "initializing tools..." + fg.rs)
pygame.mixer.init()
recognizer = sr.Recognizer()
generator = pipeline("text-generation", model="Qwen/Qwen2-1.5B")

# initializing parameters
recognizer.pause_threshold = 1.5
listening_active = True

def play_speech(text):
    """
    generate and play mp3 from text in memory
    - input: a string of text to convert to speech
    """
    # generate mp3 speech
    tts = gTTS(text=text, lang='en')
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    
    # play from memory
    pygame.mixer.music.load(mp3_fp)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # stop playing if user hits 'esc'
        if keyboard.is_pressed('esc'):
            pygame.mixer.music.stop()
            break
        time.sleep(0.05)
    mp3_fp.close()

def listen_and_respond():
    """
    collect vocal input from user and respond to it
    """
    global listening_active
    try:
        # collect microphone input
        with sr.Microphone() as source:
            print(fg.red + "listening..." + fg.rs)
            audio = recognizer.listen(source, timeout=10)
        
        # convert user speech input into text (requires internet connection)
        text = recognizer.recognize_google(audio)
        
        # if user said "exit" - stop execution!
        if text.lower() == "exit":
            return False
        
        print(fg.yellow + "you:" + fg.rs)
        print(text)
        
        # generate text response from LLM
        prompt = "Please tell me " + text
        response = generator(
            prompt, 
            max_new_tokens=50, 
            do_sample=True, 
            temperature=0.6, 
            return_full_text=False, 
            top_k=50, 
            top_p=0.95
        )[0]['generated_text']

        print(fg.green + "chatty:" + fg.rs)
        print(response)
        
        # play audio response
        play_speech(response)

    except Exception as e:
        print("Error:", str(e))
        return True

def main_loop():
    """
    run the application
    """
    global listening_active
    
    while listening_active:
        # communicate with LLM
        working = listen_and_respond()
        # if user said "exit"
        if working == False:
            print("exiting, bye bye...")
            break
        # if user pressed "esc"
        if keyboard.is_pressed('esc'):
            print("exiting, bye bye...")
            break
    pygame.mixer.quit()
    print(fg.blue + "program terminated." + fg.rs)

if __name__ == "__main__":
    main_loop()
import time, keyboard, pygame, logging,io
import speech_recognition as sr
from gtts import gTTS
from sty import fg
import requests,random
from secrets import LLM_uri


class LowLevelAPI:
    """Implement Ollama basic chatting class"""
    prompt = {
        "system_prompt": """
            You are a friendly and engaging AI designed for natural, cordial, and enjoyable conversations in various languages. 
            Your goal is to make users feel comfortable, heard, and entertained while maintaining a polite and warm tone.

            Respond in a natural, conversational manner, as if chatting with a friend.
            Adapt your tone and style based on the user's way of speaking to create a seamless and enjoyable interaction.
            Show genuine curiosity, ask relevant follow-up questions, and acknowledge what the user says to keep the conversation flowing.
            Be positive, empathetic, and open-minded. If a user shares personal experiences or emotions, respond with kindness and understanding.
            Keep responses engaging but concise—avoid overly long or robotic-sounding messages.
            Use humor and lightheartedness when appropriate, but always be respectful and considerate.
            If the user seems to want deep discussions, engage thoughtfully; if they prefer casual banter, keep it light and fun.
            Avoid controversial, argumentative, or offensive topics unless the user specifically requests a nuanced discussion in good faith.
            Your primary mission is to create an enjoyable, friendly, and relaxed conversational experience! 
        """,
        }
    
    model_list = ["phi4", "qwen2.5:0.5b","llama3.2:1b", 'gemma2:9b']

    def __init__(self, model: str = "llama3.2:1b", uri:str= None) -> None:
        self.model = model if model in self.model_list else random.choice(self.model_list)
        self.LLM_uri = LLM_uri if not uri else uri

    def call_LLM( self,user_prompt: str, system_prompt: str = prompt['system_prompt'] ) -> str: 
        common_setup = {"model": self.model, "stream": False}
        headers = None
        payload = { **common_setup, "keep_alive": 40, "system": system_prompt, "prompt": user_prompt, }
        response = requests.post(self.LLM_uri, headers=headers, json=payload)
        if response.status_code != 200:
            return f"Errore: {response.status_code} - {response.text}"
        json_response = response.json()
        json_response = json_response["response"]
        return json_response["response"] 



#################################################
# This code will work perfectly for all ollama installed models, please fille the "model_list" for increase stability
#################################################
ollama_model = LowLevelAPI('llama3.2:1b') 


# initializing tools
print(fg.blue + "initializing tools..." + fg.rs)
pygame.mixer.init()
recognizer = sr.Recognizer()

# initializing parameters
recognizer.pause_threshold = 1.5
listening_active = True

def play_speech(text : str) -> None:
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
        response = ollama_model.call_LLM(user_prompt=prompt)

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

    pygame.mixer.quit()
    print(fg.blue + "program terminated." + fg.rs)

if __name__ == "__main__":
    main_loop()
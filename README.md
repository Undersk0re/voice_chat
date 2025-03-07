# Voice Chat
a console voice chat application using small Language Models on CPU

## Run Application
please make sure a microphone is connected and available on your system before you run the following code in your console.
And sadly, Windows only! (additional setup is required to enable microphone/speaker access for WSL2/Linux systems)
```
git clone https://github.com/MariyaSha/voice_chat.git
cd voice_chat

conda create -n env_name python=3.11
conda activate env_name
pip install -r requirements.txt
python voice_chat.py
```

## Customize Application
Try different accents
```
from gtts import gTTS

text = "Hello, this is a test of different accents."

# American English (default, google.com)
tts_us = gTTS(text=text, lang='en', tld='com')
tts_us.save("hello_us.mp3")

# British English (google.co.uk)
tts_uk = gTTS(text=text, lang='en', tld='co.uk')
tts_uk.save("hello_uk.mp3")

# Australian English (google.com.au)
tts_au = gTTS(text=text, lang='en', tld='com.au')
tts_au.save("hello_au.mp3")

# Indian English (google.co.in)
tts_in = gTTS(text=text, lang='en', tld='co.in')
tts_in.save("hello_in.mp3")
```
<br>

Try different voices (instead of gTTS, using pyttsx3)
```
import pyttsx3

text = "Hello, this is a test with different voices."

# Initialize the TTS engine
engine = pyttsx3.init()

# Select Voice by Index
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Play Audio
engine.say(text)
engine.runAndWait()
```

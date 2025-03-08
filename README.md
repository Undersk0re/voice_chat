# Voice Chat
a console voice chat application using small Language Models Usin OLLAMA installed in some server (is a pre-requirement)

## Run Application
please make sure a microphone is connected and available on your system before you run the following code in your console.

```
git clone https://github.com/MariyaSha/voice_chat.git
cd voice_chat

python3 -m venv .venv_voice_chat
source .venv_voice_chat/bin/activate
pip install -r requirements.txt # or using a requirements_D.txt for a dev environment
```

If you use Windows please follow original README

If you use linux (debian) run
```
sudo apt install python3-pyaudio
```


Then you need to modify  `.venv_voice_chat/pyvenv.cfg` in this way if you have

From

```
home = /usr/bin
include-system-site-packages = false
version = 3.11.2
executable = /usr/bin/python3.11
command = /usr/bin/python3 -m venv /media/simone/USB_projects/ATTIVI/Community/voice_chat/.venv_voice_chat

```

To

```
home = /usr/bin
include-system-site-packages = true
version = 3.11.2
executable = /usr/bin/python3.11
command = /usr/bin/python3 -m venv /media/simone/USB_projects/ATTIVI/Community/voice_chat/.venv_voice_chat
```


Then you need to add your Ollama endpoint in `secrets.py`


## Customize Application
### Different Accents
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

### Different Voices
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



#### Enjoy chat (=
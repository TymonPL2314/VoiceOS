## **VoiceOS (Prototype)**



###### to jest pierwszy prototyp lokalnego asystenta głosowego **VoiceOS** opartego na Pythonie, CustomTkinter oraz API Groq (Whisper do mowy oraz LLM do odpowiedzi).

###### 

###### this is the first prototype of the local voice assistant **VoiceOS** built with Python, CustomTkinter, and the Groq API (Whisper for speech-to-text and LLM for responses).

###### 

#### **📌 Status:**

###### **\* \*\*Wersja / Version:\*\* Pierwszy prototyp / First prototype (v0.1)** 

###### **\* \*\*Języki / Languages:\*\* Działa aktualnie tylko po polsku i po angielsku / Currently works only in Polish and English.**

**\* \*\*Sterowanie / Controls:\*\* Przytrzymaj `CTRL + ALT`, powiedz coś do mikrofonu i puść – asystent przetworzy mowę i wyświetli zaokrągloną odpowiedź na pływającej wyspie. / Hold `CTRL + ALT`, speak into your microphone and release – the assistant will process your speech and display a rounded response on the floating island.


🚀 Instrukcja instalacji i uruchomienia / Installation \& Setup Guide**

---

###### **📋 Wymagania wstępne / Prerequisites**

###### **Python (zalecana wersja 3.10 lub nowsza / recommended 3.10+).**

###### 

###### **Klucz API z platformy Groq / Groq API key.**

###### 

###### **⚙️ 1. Instalacja bibliotek / Install dependencies**

###### **Otwórz terminal w folderze z projektem i wpisz / Open your project folder terminal and run:**

###### **pip install customtkinter customtkinter-stubs sounddevice numpy keyboard pillow groq**

###### 

###### **📁 2. Struktura folderów / Folder structure**

**Upewnij się, że w katalogu z plikiem voiceos.py masz folder Images z animacją / Make sure you have an Images folder with the animation next to voiceos.py:

VoiceOS**
---

###### **│**

###### **├── voiceos.py**

**├── README.md
└── Images**
---

&#x20;   **├── listening-animated.gif
    ├── listening.png
    └── response.png

🔑 3. Konfiguracja / Configuration**
---

**Wklej swój klucz API Groq w pliku voiceos.py w zmiennej GROQ\_API\_KEY / Paste your Groq API key in voiceos.py:**

---

**GROQ\_API\_KEY = "twój\_klucz\_api\_groq"

▶️ 4. Uruchomienie / Run**

---

**W CMD Napisz / In CMD Type: 

"python voiceos.py"

🎮 Jak używać? / How to use?**
---

###### **Przytrzymaj skrót CTRL + ALT i powiedz coś do mikrofonu (po polsku lub angielsku). / Hold CTRL + ALT and speak into your microphone (in Polish or English).**

###### 

###### **Puść klawisze – aplikacja przetworzy mowę i wyświetli zaokrągloną odpowiedź na pływającej wyspie. / Release the keys – the app will process your speech and display a rounded response on the floating island.**

###### 

**Kliknij myszką w dowolnym miejscu okna, aby je zamknąć. / Click anywhere on the window to close it.

🔑 Skąd wziąć API Groq? / Where you can get the Groq API?

Wejdź na strone https://console.groq.com/keys, Stwórz lub zaloguj sie na konto groq i stwórz nowe API. Nastepnie skopiuj API i wklej je do wyznaczonego miejsca w kodzie (na prawie samej górze) UWAGA!!! Kod API wyświetla sie tylko raz i nie możesz go ponownie wyświetlić. / Go to https://console.groq.com/keys, create a Groq account or log in, and generate a new API key. Then, copy the key and paste it into the designated spot in the code (near the very top). NOTE!!! The API key is displayed only once and cannot be viewed again.

============================================

ENGLISH SUPPORT WARNING!!!

============================================

The Python console does not operate in English. I recommend using a translator to understand the messages displayed in the console.**
---


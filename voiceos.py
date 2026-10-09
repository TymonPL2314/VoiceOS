import threading
import time
import os
import textwrap
import traceback
from io import BytesIO
import wave

import numpy as np
import sounddevice as sd
import customtkinter as ctk
import keyboard

from PIL import Image, ImageTk
from groq import Groq


# =========================================================
# KONFIGURACJA
# =========================================================

GROQ_API_KEY = "TWOJ_API_KLUCZ_YOUR_API_KEY"

client = Groq(
    api_key=GROQ_API_KEY
)

SAMPLE_RATE = 16000
CHANNELS = 1

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

IMAGES_DIR = os.path.join(
    BASE_DIR,
    "Images"
)

LISTENING_GIF = os.path.join(
    IMAGES_DIR,
    "listening-animated.gif"
)


# =========================================================
# ZMIENNE
# =========================================================

recording = False
audio_stream = None
audio_frames = []

app = None

conversation_history = [
    {
        "role": "system",
        "content": (
            "Jesteś inteligentnym asystentem VoiceOS "
            "na komputerze. "
            "Odpowiadaj krótko, naturalnie i po polsku. "
            "Pamiętaj poprzednią rozmowę."
        )
    }
]


# =========================================================
# GUI
# =========================================================

class VoiceOSIsland(ctk.CTk):

    def __init__(self):

        super().__init__()

        print("Tworzenie interfejsu...")

        self.overrideredirect(True)

        self.attributes(
            "-topmost",
            True
        )

        # Trik na przezroczystość/zaokrąglenie w Windowsie
        try:
            self.attributes("-transparentcolor", "#FF00FF")
            self.configure(fg_color="#FF00FF")
        except Exception:
            self.configure(fg_color="#08080A")

        self.screen_width = (
            self.winfo_screenwidth()
        )

        self.withdraw()

        # -----------------------------
        # GIF
        # -----------------------------

        self.gif_frames = []
        self.gif_delays = []
        self.gif_index = 0
        self.gif_animation_running = False
        self.gif_photo = None
        self.gif_label = None

        self.load_gif()

        # -----------------------------
        # Główna ramka z mocnym zaokrągleniem
        # -----------------------------

        self.inner_frame = ctk.CTkFrame(
            self,
            fg_color="#08080A",
            corner_radius=30,
            border_width=0
        )

        self.inner_frame.pack(
            expand=True,
            fill="both",
            padx=0,
            pady=0
        )

        # Kliknięcie gdziekolwiek chowa okno
        self.bind("<Button-1>", lambda event: self.hide())
        self.inner_frame.bind("<Button-1>", lambda event: self.hide())

        print("Interfejs gotowy.")

    # =====================================================
    # ŁADOWANIE GIF
    # =====================================================

    def load_gif(self):

        if not os.path.exists(
            LISTENING_GIF
        ):

            print(
                "UWAGA! Nie znaleziono GIF:"
            )

            print(
                LISTENING_GIF
            )

            return

        try:

            gif = Image.open(
                LISTENING_GIF
            )

            self.gif_frames = []
            self.gif_delays = []

            for i in range(
                gif.n_frames
            ):

                gif.seek(i)

                frame = gif.convert(
                    "RGBA"
                )

                self.gif_frames.append(
                    frame.copy()
                )

                delay = gif.info.get(
                    "duration",
                    80
                )

                if delay <= 0:
                    delay = 80

                self.gif_delays.append(
                    delay
                )

            print(
                "GIF załadowany:",
                len(self.gif_frames),
                "klatek"
            )

        except Exception as e:

            print(
                "Błąd GIF:",
                e
            )

    # =====================================================
    # ANIMACJA GIF
    # =====================================================

    def animate_gif(self):

        if not self.gif_animation_running:
            return

        if not self.gif_frames:
            return

        try:

            frame = self.gif_frames[
                self.gif_index
            ]

            frame = frame.resize(
                (130, 46),
                Image.Resampling.LANCZOS
            )

            self.gif_photo = ImageTk.PhotoImage(
                frame
            )

            if self.gif_label:

                self.gif_label.configure(
                    image=self.gif_photo
                )

            delay = self.gif_delays[
                self.gif_index
            ]

            self.gif_index += 1

            if self.gif_index >= len(
                self.gif_frames
            ):

                self.gif_index = 0

            self.after(
                delay,
                self.animate_gif
            )

        except Exception:

            traceback.print_exc()

    # =====================================================
    # POKAŻ STAN "SŁUCHAM..."
    # =====================================================

    def show_listening(self):
        self.after(0, self._show_listening)

    def _show_listening(self):
        try:
            width = 160
            height = 50

            x = (self.screen_width - width) // 2
            y = 18

            self.geometry(f"{width}x{height}+{x}+{y}")
            self.gif_animation_running = False

            for widget in self.inner_frame.winfo_children():
                widget.destroy()

            self.inner_frame.configure(fg_color="#08080A")

            self.gif_label = ctk.CTkLabel(
                self.inner_frame,
                text=""
            )
            self.gif_label.pack(expand=True, fill="both")
            self.gif_label.bind("<Button-1>", lambda event: self.hide())

            self.gif_index = 0
            self.gif_animation_running = True

            self.deiconify()
            self.lift()

            if self.gif_frames:
                self.animate_gif()
            else:
                self.gif_label.configure(
                    text="SŁUCHAM...",
                    text_color="#00E5FF",
                    font=("Segoe UI", 13, "bold")
                )

        except Exception:

            traceback.print_exc()

    # =====================================================
    # POKAŻ ODPOWIEDŹ
    # =====================================================

    def show_response(
        self,
        text,
        width=440
    ):

        self.after(
            0,
            lambda: self._show_response(
                text,
                width
            )
        )

    def _show_response(
        self,
        text,
        width
    ):

        try:

            chars_per_line = max(
                30,
                int(width / 9)
            )

            lines = textwrap.wrap(
                text,
                width=chars_per_line
            )

            number_of_lines = max(
                1,
                len(lines)
            )

            height = max(
                100,
                number_of_lines * 24 + 50
            )

            height = min(
                height,
                500
            )

            x = (
                self.screen_width - width
            ) // 2

            y = 18

            self.geometry(
                f"{width}x{height}+{x}+{y}"
            )

            self.gif_animation_running = False

            for widget in (
                self.inner_frame.winfo_children()
            ):

                widget.destroy()

            self.inner_frame.configure(
                fg_color="#08080A"
            )

            self.label = ctk.CTkLabel(
                self.inner_frame,
                text=text,
                text_color="#F5F5F7",
                font=(
                    "Segoe UI",
                    15
                ),
                justify="left",
                anchor="center",
                wraplength=width - 48,
                fg_color="transparent",
                width=width - 48,
                height=height - 36
            )

            self.label.place(
                x=24,
                y=18
            )

            self.label.bind("<Button-1>", lambda event: self.hide())

            self.deiconify()

            self.lift()

        except Exception:

            traceback.print_exc()

    # =====================================================
    # UKRYJ
    # =====================================================

    def hide(self):

        self.after(
            0,
            self.withdraw
        )


# =========================================================
# URUCHOMIENIE GUI
# =========================================================

def run_gui():

    global app

    try:

        print(
            "Uruchamianie GUI..."
        )

        ctk.set_appearance_mode(
            "dark"
        )

        app = VoiceOSIsland()

        print(
            "GUI działa."
        )

        app.show_response("VoiceOS gotowy. Przytrzymaj CTRL+ALT żeby mówić.")

        app.mainloop()

    except Exception:

        print(
            "BŁĄD GUI:"
        )

        traceback.print_exc()


# =========================================================
# MIKROFON & AUDIO CALLBACK
# =========================================================

def audio_callback(indata, frames, time_info, status):
    if status:
        print("Audio status:", status)
    if recording:
        audio_frames.append(indata.copy())


def start_recording():
    global recording, audio_frames, audio_stream

    if recording:
        return

    print("Rozpoczynam nasłuch z mikrofonu...")
    recording = True
    audio_frames = []

    if app:
        app.show_listening()

    try:
        audio_stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="float32",
            callback=audio_callback
        )
        audio_stream.start()
    except Exception as e:
        print("BŁĄD MIKROFONU:", e)
        recording = False
        audio_stream = None


def stop_recording():
    global recording, audio_stream

    if not recording:
        return

    print("Kończę nagrywanie...")
    recording = False

    try:
        if audio_stream:
            audio_stream.stop()
            audio_stream.close()
            audio_stream = None
    except Exception as e:
        print("Błąd zamykania mikrofonu:", e)

    threading.Thread(
        target=process_recording,
        daemon=True
    ).start()


# =========================================================
# PRZETWARZANIE NAGRANIA (WHISPER + GROQ)
# =========================================================

def process_recording():
    global audio_frames, conversation_history

    try:
        print("Przetwarzanie audio...")

        if not audio_frames:
            print("Brak nagrania.")
            if app:
                app.hide()
            return

        frames_copy = list(audio_frames)
        audio_frames = []

        audio_data = np.concatenate(frames_copy, axis=0)

        wav_io = BytesIO()
        with wave.open(wav_io, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(2)
            wf.setframerate(SAMPLE_RATE)
            pcm = (audio_data * 32767).clip(-32768, 32767).astype(np.int16)
            wf.writeframes(pcm.tobytes())

        wav_io.seek(0)

        print("Wysyłam audio do Whisper...")
        transcription = client.audio.transcriptions.create(
            file=("voiceos.wav", wav_io.read(), "audio/wav"),
            model="whisper-large-v3",
            language="pl"
        )

        user_text = transcription.text.strip()
        print("Usłyszano:", user_text)

        if not user_text:
            if app:
                app.hide()
            return

        conversation_history.append(
            {
                "role": "user",
                "content": user_text
            }
        )

        if len(conversation_history) > 15:
            conversation_history = (
                [conversation_history[0]]
                + conversation_history[-14:]
            )

        print("Wysyłam zapytanie do AI...")
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=conversation_history,
            temperature=0.7,
            max_tokens=500
        )

        assistant_text = (
            response.choices[0]
            .message
            .content
            .strip()
        )

        conversation_history.append(
            {
                "role": "assistant",
                "content": assistant_text
            }
        )

        if app:
            app.show_response(assistant_text)

    except Exception:
        traceback.print_exc()
        if app:
            app.show_response("Wystąpił błąd przetwarzania mowy 💀")


# =========================================================
# OBSŁUGA KLAWIATURY (CTRL + ALT)
# =========================================================

def watch_keys():
    print("Nasłuchiwanie skrótu Ctrl+Alt...")
    previous_state = False

    while True:
        try:
            current_state = (
                keyboard.is_pressed("ctrl")
                and keyboard.is_pressed("alt")
            )

            if current_state and not previous_state:
                start_recording()

            if not current_state and previous_state:
                stop_recording()

            previous_state = current_state
            time.sleep(0.03)

        except Exception:
            print("Błąd klawiatury:")
            traceback.print_exc()
            time.sleep(1)


# =========================================================
# MAIN
# =========================================================

def main():

    print()
    print(
        "==============================================================="
    )
    print(
        "          VoiceOS Working Press CTRL + ALT"
    )
    print(
        "=============================================================="
    )

    print(
        "Folder programu:"
    )
    print(
        BASE_DIR
    )

    print(
        "Folder obrazów:"
    )
    print(
        IMAGES_DIR
    )
    print()

    keyboard_thread = threading.Thread(
        target=watch_keys,
        daemon=True
    )
    keyboard_thread.start()
    print("Wątek klawiatury uruchomiony.")

    run_gui()


if __name__ == "__main__":

    try:
        main()
    except KeyboardInterrupt:
        print("VoiceOS zatrzymany.")
    except Exception:
        traceback.print_exc()
        input("Naciśnij ENTER...")

# ==============================================================
#      !!!               KONIEC KODU                !!!
# ==============================================================

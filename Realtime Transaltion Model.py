import tkinter as tk
from tkinter import ttk, messagebox
from googletrans import Translator
from gtts import gTTS
from playsound import playsound
import os
import pyttsx3
import speech_recognition as sr
from ttkbootstrap import Style


class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Translator")
        self.root.geometry("415x430")

        self.destination_language_var = tk.StringVar()
        self.voice_var = tk.StringVar(value="1")  # Default value set to "1"
        self.input_type_var = tk.StringVar(value="Text")

        self.create_widgets()

    def create_widgets(self):

        # Apply ttkbootstrap theme
        style = Style(theme='superhero')  # You can choose any theme you prefer (darkly,solar)

        # Destination Language Selection
        language_label = ttk.Label(self.root, text="Select Destination Language:")
        language_label.grid(row=0, column=0, padx=10, pady=25, sticky="w")

        self.language_entry = ttk.Entry(self.root, textvariable=self.destination_language_var)
        self.language_entry.grid(row=0, column=1, padx=10, pady=5)

        # Voice Selection
        voice_label = ttk.Label(self.root, text="Choose Voice (1 for Female, 2 for Male):")
        voice_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.voice_entry = ttk.Combobox(self.root, textvariable=self.voice_var, values=["1", "2"])
        self.voice_entry.grid(row=1, column=1, padx=10, pady=5)

        # Input Type Selection
        input_type_label = ttk.Label(self.root, text="Choose Input Type:")
        input_type_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.input_type_combobox = ttk.Combobox(self.root, textvariable=self.input_type_var, values=["Text", "Speech"], state="readonly")
        self.input_type_combobox.grid(row=2, column=1, padx=10, pady=5)
        self.input_type_combobox.bind("<<ComboboxSelected>>", self.on_input_type_change)

        # Input Text
        self.input_text_label = ttk.Label(self.root, text="Enter the text you want to translate:")
        self.input_text_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.input_text_entry = ttk.Entry(self.root,font=("Helvetica",20), width=25)
        self.input_text_entry.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        # Translate Button
        self.style = ttk.Style()
        self.style.configure("danger.TButton",font=("Helvetica",15))
        self.translate_button = ttk.Button(self.root, width=10, style="danger.TButton", text="Translate", command=self.translate_text)
        self.translate_button.grid(row=5, columnspan=2, padx=10, pady=10)

        # Speak Button
        self.style = ttk.Style()
        self.style.configure("success.TButton",font=("Helvetica",15))
        self.speak_button = ttk.Button(self.root,width=10, style="success.TButton", text="Speak", command=self.record_and_translate)
        self.speak_button.grid(row=5, columnspan=2, padx=10, pady=10)
        self.speak_button.grid_remove()  # Hide the Speak button initially

        # Translated Text Display
        self.translated_text_label = ttk.Label(self.root, text="Translated Text:")
        self.translated_text_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")

        self.translated_text_display = tk.Text(self.root, height=5, width=50)
        self.translated_text_display.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

    def on_input_type_change(self, event):
        input_type = self.input_type_var.get()
        if input_type == "Speech":
            self.input_text_entry.config(state="disabled")
            self.translate_button.grid_remove()  # Hide the Translate button
            self.speak_button.grid()  # Show the Speak button
        else:
            self.input_text_entry.config(state="normal")
            self.translate_button.grid()  # Show the Translate button
            self.speak_button.grid_remove()  # Hide the Speak button

    def translate_text(self):
        destination_language = self.destination_language_var.get()
        input_type = self.input_type_var.get()

        if not destination_language:
            messagebox.showwarning("Warning", "Please enter destination language.")
            return
        if not input_type:
            messagebox.showwarning("Warning", "Please select input type.")
            return

        try:
            voice_choice = int(self.voice_var.get())
        except ValueError:
            messagebox.showwarning("Warning", "Invalid choice for voice.")
            return

        if input_type == "Text":
            input_text = self.input_text_entry.get()
            if not input_text:
                messagebox.showwarning("Warning", "Please enter text to translate.")
                return
            translated_text = self.translate(input_text, destination_language)
            self.show_translation(translated_text)
            self.play_sound(translated_text, voice_choice, destination_language)
        else:  # Speech
            self.record_and_translate()

    def translate(self, text, destination_language):
        translator = Translator()
        translation = translator.translate(text, dest=destination_language)
        return translation.text

    def show_translation(self, translated_text):
        self.translated_text_display.delete(1.0, tk.END)
        self.translated_text_display.insert(tk.END, translated_text)

    def play_sound(self, text, voice_choice, destination_language):
        if voice_choice == 1:
            lang = destination_language
        elif voice_choice == 2:
            lang = 'en-au'
        else:
            lang = 'en-in'

        tts = gTTS(text=text, lang=lang)
        filename = "translated_audio.mp3"
        tts.save(filename)
        playsound(filename)
        os.remove(filename)  # Remove the file after playing

    def record_and_translate(self):
        destination_language = self.destination_language_var.get()  # Get the destination language
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 0.5
            audio = r.listen(source)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"The User said: {query}\n")
            translated_text = self.translate(query, destination_language)
            self.show_translation(translated_text)
            self.play_sound(translated_text, int(self.voice_var.get()), destination_language)
        except Exception as e:
            messagebox.showerror("Error", "Couldn't recognize speech. Please try again.")

def main():
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()




import speech_recognition as sr
import webbrowser
import pyttsx3
import ollama
import requests

class Jarvis:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.is_running = True

        print("[Calibrating microphone...]")
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        print(f"[Calibration done! Threshold: {self.recognizer.energy_threshold}]")


        self.chat_history = [{
            "role": "system",
            "content": "You are Jarvis, a helpful voice assistant. Keep answers short."
        }]

    def speak(self, text):
        try:
            print(f"Jarvis: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Speech error: {e}")

    def listen(self, timeout=10, phrase_limit=8):
        try:
            with sr.Microphone() as source:
                audio = self.recognizer.listen(source,
                            timeout=timeout,
                            phrase_time_limit=phrase_limit)
                return self.recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return None
        except sr.WaitTimeoutError:
            return None
        except sr.RequestError as e:
            print(f"Error: {e}")
            return None
        except Exception as e:
            print(f"Listen error: {e}")
            return None

    def get_weather(self, city):
        try:
            api_key = "Your_api_key"
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": city,
                "appid": api_key,
                "units": "metric"
            }
            print(f"[Getting weather for: {city}]")
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()

            city_name   = data["name"]
            temp        = data["main"]["temp"]
            description = data["weather"][0]["description"]
            humidity    = data["main"]["humidity"]

            self.speak(f"Weather in {city_name}")
            self.speak(f"Temperature is {temp} degrees celsius")
            self.speak(f"Condition is {description}")
            self.speak(f"Humidity is {humidity} percent")

        except requests.exceptions.ConnectionError:
            self.speak("No internet connection")
        except requests.exceptions.RequestException as e:
            print(f"Weather error: {e}")
            self.speak("Could not get weather")

    def ask_ai(self, question):
        try:
            print(f"[Asking AI: {question}]")
            self.speak("Let me think...")

            self.chat_history.append({"role": "user","content": question})

            response = ollama.chat(
                model="llama3.2:3b",
                messages=self.chat_history
            )

            answer = response["message"]["content"]

            self.chat_history.append({
                "role": "assistant",
                "content": answer
            })

        
            if len(self.chat_history) > 21:
                self.chat_history = [self.chat_history[0]] + self.chat_history[-20:]

            print(f"[AI]: {answer}")
            self.speak(answer)

        except Exception as e:
            print(f"AI error: {e}")
            self.speak("Sorry, could not get a response")

    def process_command(self, c):
        print(f"\n>>> COMMAND: '{c}'")
        c_lower = c.lower()

        if "google" in c_lower and "search" not in c_lower:
            self.speak("Opening Google")
            webbrowser.open("https://google.com")

        elif "youtube" in c_lower and "play" not in c_lower:
            self.speak("Opening YouTube")
            webbrowser.open("https://youtube.com")

        elif "whatsapp" in c_lower:
            self.speak("Opening WhatsApp")
            webbrowser.open("https://web.whatsapp.com/")

        elif "play" in c_lower:
            song = c_lower.replace("play", "").strip()
            self.speak(f"Playing {song}")
            webbrowser.open("https://www.youtube.com/results?search_query=" + song.replace(" ", "+"))

        elif "search" in c_lower:
            query = c_lower.replace("search", "").strip()
            if query:
                self.speak(f"Searching {query} on Google")
                webbrowser.open("https://www.google.com/search?q=" + query.replace(" ", "+"))
            else:
                self.speak("What would you like me to search?")

        elif "weather" in c_lower:
            words = c_lower.split()
            if "in" in words:
                city = " ".join(words[words.index("in") + 1:])
            elif "of" in words:
                city = " ".join(words[words.index("of") + 1:])
            else:
                city = c_lower.replace("weather", "").strip()
            if city:
                self.get_weather(city)
            else:
                self.speak("Which city's weather would you like to know?")

        elif "stop" in c_lower or "exit" in c_lower or "bye" in c_lower:
            self.speak("Goodbye! Shutting down Jarvis!")
            self.is_running = False
            return "exit"    

        else:
            self.ask_ai(c)

    def command_loop(self):
     
        self.speak("Yes! I am listening!")
        print("[Command mode — say 'bye' or 'exit' to stop]")

        while self.is_running:
            print("\n[Waiting for command...]")
            command = self.listen(timeout=10, phrase_limit=10)

            if command is None:
                print("[Nothing heard...]")
                self.speak("I am still here!")
                continue

            print(f"[Command: {command}]")
            result = self.process_command(command)

            if result == "exit":
                break    
    def run(self):
        print("Starting Jarvis 2.0...")
        self.speak("Initializing Jarvis 2.0")

        while self.is_running:
            print("\n[Listening for wake word...]")
            word = self.listen(timeout=10, phrase_limit=5)

            if word is None:
                print("[Nothing heard, listening again...]")
                continue

            if "jarvis" in word.lower():
                self.command_loop()    # ← enters command loop

        print("Jarvis shutdown complete!")


if __name__ == "__main__":
    jarvis = Jarvis()
    jarvis.run()
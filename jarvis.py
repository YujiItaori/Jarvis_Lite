# jarvis.py
import pyttsx3
import speech_recognition as sr
import webbrowser
import subprocess
import sys
import os
import datetime
import requests
import json
import random
import wikipedia
from fuzzywuzzy import fuzz
import time
from bs4 import BeautifulSoup

class JarvisEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.setup_voice()
        self.jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a fake noodle? An impasta!",
            "Why did the scarecrow win an award? He was outstanding in his field!"
        ]
        
    def setup_voice(self):
        """Configure voice settings"""
        voices = self.engine.getProperty('voices')
        if voices:
            # Try to set a better voice if available
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
        
        # Set speech rate and volume
        self.engine.setProperty('rate', 180)  # Speed of speech
        self.engine.setProperty('volume', 0.8)  # Volume level
    
    

    def speak(self, text):
        """Enhanced speak function with error handling"""
        try:
            print(f"🤖 Jarvis: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Speech error: {e}")

    def listen_with_timeout(self, timeout=5):
        """Enhanced listening with better error handling"""
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 300
        recognizer.dynamic_energy_threshold = True
        
        try:
            with sr.Microphone() as source:
                print("🎤 Listening...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=5)
            
            command = recognizer.recognize_google(audio)
            print(f"📥 Heard: {command}")
            return command.lower()
        except sr.WaitTimeoutError:
            return "timeout"
        except sr.UnknownValueError:
            return "unclear"
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            return None

    def open_application(self, app_name):
        """Open applications based on OS"""
        app_name = app_name.lower()
        
        if sys.platform.startswith('win'):
            apps = {
                'notepad': 'notepad.exe',
                'calculator': 'calc.exe',
                'paint': 'mspaint.exe',
                'explorer': 'explorer.exe',
                'chrome': 'chrome.exe',
                'firefox': 'firefox.exe'
            }
            
            if app_name in apps:
                try:
                    subprocess.Popen(apps[app_name])
                    return f"Opening {app_name.title()}"
                except FileNotFoundError:
                    return f"Could not find {app_name}"
        
        return f"Application opening not supported for {app_name}"

    def get_weather(self, city=""):
        """Get weather information (requires API key)"""
        # This is a placeholder - you'd need to implement with a weather API
        return f"I'd need a weather API key to get current weather information. You can get one from OpenWeatherMap."

    def search_wikipedia(self, query):
        """Search Wikipedia for information"""
        try:
            summary = wikipedia.summary(query, sentences=2)
            return f"According to Wikipedia: {summary}"
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Multiple results found for {query}. Try being more specific."
        except wikipedia.exceptions.PageError:
            return f"No Wikipedia page found for {query}."
        except Exception as e:
            return f"Sorry, I couldn't search Wikipedia right now."

    def get_time(self):
        """Get current time"""
        now = datetime.datetime.now()
        return f"The current time is {now.strftime('%I:%M %p')}"

    def get_date(self):
        """Get current date"""
        now = datetime.datetime.now()
        return f"Today is {now.strftime('%A, %B %d, %Y')}"

    def tell_joke(self):
        """Tell a random joke"""
        return random.choice(self.jokes)

    def calculate(self, expression):
        """Simple calculator"""
        try:
            # Remove 'calculate' and common words
            expression = expression.replace('calculate', '').replace('what is', '').strip()
            
            # Replace words with operators
            expression = expression.replace('plus', '+').replace('minus', '-')
            expression = expression.replace('times', '*').replace('divided by', '/')
            expression = expression.replace('multiplied by', '*')
            
            # Simple eval for basic math (be careful with eval in production!)
            result = eval(expression)
            return f"The answer is {result}"
        except:
            return "I couldn't calculate that. Please try a simpler expression."

    def fuzzy_match_command(self, command, threshold=70):
        """Use fuzzy matching to handle variations in commands"""
        commands = {
            'hello': ['hello', 'hi', 'hey', 'greetings'],
            'time': ['time', 'what time', 'current time'],
            'date': ['date', 'what date', 'today'],
            'weather': ['weather', 'temperature', 'forecast'],
            'joke': ['joke', 'funny', 'make me laugh'],
            'youtube': ['youtube', 'videos'],
            'google': ['google', 'search'],
            'wikipedia': ['wikipedia', 'wiki', 'information about'],
            'calculate': ['calculate', 'math', 'compute'],
            'music': ['music', 'play music', 'songs']
        }
        
        best_match = None
        best_score = 0
        
        for category, variations in commands.items():
            for variation in variations:
                score = fuzz.ratio(command, variation)
                if score > best_score and score >= threshold:
                    best_score = score
                    best_match = category
        
        return best_match, best_score

    def handle_command(self, command):
        """Enhanced command handling with fuzzy matching and more features"""
        if not command or command in ['timeout', 'unclear']:
            if command == 'timeout':
                return "I didn't hear anything. Please try again."
            elif command == 'unclear':
                return "I couldn't understand that clearly. Please try again."
            else:
                return "Sorry, I didn't receive a command."

        command = command.lower().strip()
        
        # Direct pattern matching first
        if any(word in command for word in ['hello', 'hi', 'hey']):
            return f"Hello! I'm Jarvis, your personal assistant. How can I help you today?"

        elif 'time' in command:
            return self.get_time()

        elif 'date' in command or 'today' in command:
            return self.get_date()

        elif 'joke' in command or 'funny' in command:
            return self.tell_joke()

        elif 'weather' in command:
            return self.get_weather()

        elif 'calculate' in command or any(op in command for op in ['+', '-', '*', '/', 'plus', 'minus']):
            return self.calculate(command)

        elif 'wikipedia' in command or 'wiki' in command:
            query = command.replace('wikipedia', '').replace('wiki', '').replace('search', '').strip()
            if query:
                return self.search_wikipedia(query)
            return "What would you like me to search on Wikipedia?"

        elif 'open youtube' in command:
            self.open_in_chrome("https://www.youtube.com")
            return "Opening YouTube for you."

        elif 'open google' in command:
            self.open_in_chrome("https://www.google.com")
            return "Opening Google."

        elif 'search google for' in command or 'google search' in command:
            search_term = command.replace('search google for', '').replace('google search', '').strip()
            if search_term:
                self.open_in_chrome(f"https://www.google.com/search?q={search_term}")
                return f"Searching Google for {search_term}."
            return "What would you like me to search for?"

        elif 'music' in command or 'play music' in command:
            self.open_in_chrome("https://www.spotify.com")
            return "Opening Spotify for music."

        elif 'open' in command and any(app in command for app in ['notepad', 'calculator', 'paint']):
            for app in ['notepad', 'calculator', 'paint']:
                if app in command:
                    return self.open_application(app)

        elif 'open' in command and '.com' in command:
            domain = command.split('open')[-1].strip()
            if not domain.startswith('http'):
                domain = f"https://{domain}"
            self.open_in_chrome(domain)
            return f"Opening {domain}"

        elif 'shutdown' in command or 'quit' in command:
            return "Goodbye! Have a great day!"

        # Fuzzy matching for unrecognized commands
        match, score = self.fuzzy_match_command(command)
        if match:
            return f"Did you mean to ask about {match}? (Confidence: {score}%) Please try rephrasing."

        return "I'm not sure how to help with that. Try asking about time, weather, jokes, or opening websites."

    def open_in_chrome(self, url):
        """Enhanced browser opening with better error handling"""
        chrome_paths = []
        
        if sys.platform.startswith('win'):
            chrome_paths = [
                "C:/Program Files/Google/Chrome/Application/chrome.exe",
                "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
                os.path.expanduser("~/AppData/Local/Google/Chrome/Application/chrome.exe")
            ]
        elif sys.platform.startswith('darwin'):  # macOS
            chrome_paths = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
        else:  # Linux
            chrome_paths = ["/usr/bin/google-chrome", "/usr/bin/chromium-browser"]

        for chrome_path in chrome_paths:
            if os.path.exists(chrome_path):
                try:
                    subprocess.Popen([chrome_path, url])
                    return
                except Exception as e:
                    continue
        
        # Fallback to default browser
        webbrowser.open(url)
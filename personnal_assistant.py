import speech_recognition as sr
import os
import pygame
from gtts import gTTS
from io import BytesIO
import lib.notes as notes
import lib.email as email
from datetime import datetime

# This function initiate a new sr instance and clean the audio var

def initiate_listener(index = 0):
    r = sr.Recognizer()
    if index == 0:
        index = int(choose_mic())
    mic = sr.Microphone(device_index=index)
    return r,mic, index

# The user choose a microphone thanks to the list diplayed and the corresponding index

def choose_mic():
    print("Choose a microphone from the list")
    print(sr.Microphone.list_microphone_names())
    index = input("Device index : ")

    return index

# This function initiate a new meeting and listen to the user to create a note

def new_meeting():
    
    print("New meeting launched")
    meeting = Meeting()
    new_meeting_indic = 1
    
    #Choosing language for this meeting
    meeting.choose_language()
    
    #Creating note file
    notes.start_note()
    
    r,mic, index = initiate_listener(meeting.mic_index)
    
    # Display key words to take new notes
    meeting.display_key_words()
    
    while new_meeting_indic == 1:
        with mic as source:
            print("listening...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            try:
                print(r.recognize_google(audio, language = meeting.SRlanguage).lower())
                
                #The user wants to take a note
                if meeting.new_note in r.recognize_google(audio, language = meeting.SRlanguage).lower():
                    meeting.take_note()
                    meeting.display_key_words()
                    
                #The user wants to stop the program
                elif meeting.stop_program in r.recognize_google(audio, language = meeting.SRlanguage).lower():
                    new_meeting_indic = 3
                
                #The user wants to end the meeting
                elif meeting.end_meeting in r.recognize_google(audio, language = meeting.SRlanguage).lower():
                    new_meeting_indic = 0
                    meeting_notes = notes.read_note()
                    dateTimeObj = datetime.now()
                    timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M)")
                    email.new_mailto("Meeting du " + timestampStr, meeting_notes)
                    notes.delete_note()
            except sr.UnknownValueError:
                print("Unknown value, not writting")
                pass
            
    print("End of the meeting.")
    return new_meeting_indic

class Meeting:
    
    def __init__(self):
        self.language = "en"
        self.SRlanguage = "en-EN"
        self.new_note = "sum up"
        self.subject = "subject"
        self.bulletPoint = "point"
        self.end_note = "noted"
        self.end_meeting = "end meeting"
        self.stop_program = "stop the program"
        self.mic_index = 0

    def display_key_words(self):
        print(" ")
        print("==========================================")
        print("To take a new note say : " + self.new_note) 
        print("To write a title say : " + self.subject) 
        print("To write a bullet point say : " + self.bulletPoint) 
        print("To pause the writting say : " + self.end_note) 
        print("To end the meeting say : " + self.end_meeting) 
        print("==========================================")
        print(" ")

    # This function is used as talking-to-user bot
    
    def text_to_speech(self,string):
        #Text-to-speech gTTS module
        mp3_fp = BytesIO()
        tts = gTTS(text=string, lang = self.language)
        tts.write_to_fp(mp3_fp)

        #Play the registered sound with pyglet
        pygame.mixer.init()
        mp3_fp.seek(0)
        pygame.mixer.music.load(mp3_fp)
        pygame.mixer.music.play()
        
        print(string)
    
    # This function is used to define meeting's language
    
    def choose_language(self):
        #init
        r,mic, index = initiate_listener()
        self.mic_index = index

        #Choose a language
        language=""
        self.text_to_speech('Please, say "I speak French" or "I speak English", to choose your language')
        while language == "":
            with mic as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                print("listening")
                try:
                    print(r.recognize_google(audio, language = self.SRlanguage).lower())
                    if "french" in r.recognize_google(audio).lower():
                        self.language = "fr"  
                        self.SRlanguage = "fr-FR"
                        self.new_note = "résum"
                        self.end_note = "noté" 
                        self.subject = "sujet"
                        self.end_meeting = "fin du meeting"
                        self.stop_program = "arrêter le programme"
                        language = "français"
                        choosed_language = "Votre assistant vocal parle maintenant " + language
                        self.text_to_speech(choosed_language)
                    if "english" in r.recognize_google(audio).lower():
                        language = "english"
                        choosed_language = language + " is now in use "
                        self.text_to_speech(choosed_language)
                except sr.UnknownValueError:
                    print("Unknown value")
        r = None
        mic = None
  
    # This function allow user to take notes and write it down into notes.txt
    
    def take_note(self):
        
        #Init_listener
        r,mic, index = initiate_listener(self.mic_index)
        
        print("Writting...")
        end_note = 0
        
        while end_note == 0:
            with mic as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                try:
                    if self.end_note in r.recognize_google(audio, language = self.SRlanguage).lower():
                        print("End writting.")
                        end_note = 1
                    elif self.subject in r.recognize_google(audio, language = self.SRlanguage).lower():
                        print("New subject : " + r.recognize_google(audio, language = self.SRlanguage))
                        notes.append_note(r.recognize_google(audio, language = self.SRlanguage), 1)
                    elif self.bulletPoint in r.recognize_google(audio, language = self.SRlanguage).lower():
                        print("New bullet point : " + r.recognize_google(audio, language = self.SRlanguage))
                        notes.append_note(r.recognize_google(audio, language = self.SRlanguage), 2)
                    else:
                        print("New note : " + r.recognize_google(audio, language = self.SRlanguage))
                        notes.append_note(r.recognize_google(audio, language = self.SRlanguage))
                except sr.UnknownValueError:
                    pass

# Main program

if __name__ == '__main__':
    
    new_meeting_indic = 0
    r,mic, index = initiate_listener()

    while new_meeting_indic == 0:
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            try:
                print('To launch a meeting say : Initiate a new meeting')
                if "new meeting" in r.recognize_google(audio).lower():
                    new_meeting_indic = new_meeting()
                elif "stop the program" in r.recognize_google(audio).lower():
                    new_meeting_indic = 3
            except sr.UnknownValueError:
                print("Still not in a meeting")

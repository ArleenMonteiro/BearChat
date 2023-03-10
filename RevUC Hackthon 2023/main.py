
#from neuralintents import GenericAssistant
import numpy as np
import tflearn as tfl
import tensorflow
import random as rn
import pickle as pi
import json
import speech_recognition
import pyttsx3
import nltk
from nltk.stem.lancaster import LancasterStemmer
#from fastapi import FastAPI, File, UploadFile
import datetime
#import wikipedia as wp
import webbrowser
import time
import subprocess
#import ecapture as ec
#import wolframalpha as wra
import sys
import os
#import pycountry
import pytz
import requests
import feedparser
import re
import pywhatkit
import googlesearcher
#import uvicorn

#pp = FastAPI()

# from flask import Flask, request
# from Website import create_app
#
# app = create_app()
#
# if __name__ == '__main__':
#     app.run(debug=True)

# @app.route('/')
# def index():
#     return '''
#         <html>
#         <body>
#             <h1>Record Audio</h1>
#             <iframe src="/record" style="border:none;width:400px;height:200px;"></iframe>
#         </body>
#         </html>
#     '''
#
# @app.route('/record')
# def record():
#     return app.send_static_file('record.html')
#
# @app.route('/upload-audio', methods=['POST'])
# def upload_audio():
#     audio_file = request.files['audio']
#
#     return 'Audio file received'
#
# if __name__ == '__main__':
#     app.run(debug=True)
#


stemmer = LancasterStemmer()
Cont = True
recognizer = speech_recognition.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 145)

# #@app.get("/")
# def test():
#     msg = "Is it right?"
#     return {"msg": msg}

# #@app.post("/process_audio")
# def process_audio(audio: UploadFile = File(...)):
#     audio_file = speech_recognition.AudioFile(audio.file)
#     with audio_file as source:
#         audio_data = recognizer.record(source)
#     text = recognizer.recognize_google(audio_data)
#     return {"message": text}

# if __name__ == '__main__':
#     uvicorn.run(app, host="0.0.0.0", port=8000)

def bot_talk(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

def greetings():
    bot_talk("Hi, This is The Bearcat ChatBot")
    bot_talk("How Can I Help You?")

def quit():
    global Cont
    Cont = False
    bot_talk("It was nice talking to you!")
    bot_talk("Hope you have a great day ahead!")
    # sys.exit()
    # os._exit()

# mappings = {
#     "greeting" : greetings,
#     "goodbye" : quit
# }

with open("intents.json") as file:
    global data
    data = json.load(file)
try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pi.load(f)
except:
    #print(data["intents"])
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?" or w != "is" or w != "the"]
    words = sorted(list(set(words)))
    labels = sorted(labels)

    # Training and Testing Outputs
    # one hot encoded
    training = []
    output = []
    out_empty = [0 for _ in range(len(labels))]

    for x,doc in enumerate(docs_x):
        bag = []
        wrds = [stemmer.stem(w.lower()) for w in doc]
        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)

    with open("data.pickle", "wb") as f:
        pi.dump((words, labels, training, output), f)

#Starting the tensorflow modelling
#tensorflow.reset_default_graph()
tensorflow.compat.v1.reset_default_graph()

net = tfl.input_data(shape=[None, len(training[0])])
net = tfl.fully_connected(net, 8)
net = tfl.fully_connected(net, 8)
net = tfl.fully_connected(net, 8)
net = tfl.fully_connected(net, 8)
# net = tfl.fully_connected(net, 8)
# net = tfl.fully_connected(net, 8)
# net = tfl.fully_connected(net, 8)
# net = tfl.fully_connected(net, 8)
net = tfl.fully_connected(net, len(output[0]), activation="softmax")
net = tfl.regression(net)

model = tfl.DNN(net)

try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=15000, batch_size=8, show_metric=True)
    model.save("model.tflearn")
    #net = tfl.fully_connected(net, 8)

# # import torch
# # import torch.nn as nn
# # import torch.optim as optim
#
# input_size = len(training[0])
# output_size = len(output[0])
#
# class NeuralNet(nn.Module):
#     def __init__(self):
#         super(NeuralNet, self).__init__()
#         self.fc1 = nn.Linear(input_size, 8)
#         self.fc2 = nn.Linear(8, 8)
#         self.fc3 = nn.Linear(8, 8)
#         self.fc4 = nn.Linear(8, output_size)
#         self.softmax = nn.Softmax(dim=1)
#
#     def forward(self, x):
#         x = torch.relu(self.fc1(x))
#         x = torch.relu(self.fc2(x))
#         x = torch.relu(self.fc3(x))
#         x = self.softmax(self.fc4(x))
#         return x
#
# model = NeuralNet()
# criterion = nn.BCELoss()
# optimizer = optim.SGD(model.parameters(), lr=0.01)
#
# try:
#     model.load_state_dict(torch.load("model.pth"))
# except:
#     for epoch in range(6000):
#         inputs = torch.Tensor(training)
#         targets = torch.Tensor(output)
#         optimizer.zero_grad()
#         outputs = model(inputs)
#         loss = criterion(outputs, targets)
#         loss.backward()
#         optimizer.step()
#         if epoch % 100 == 0:
#             print(f"Epoch {epoch+1}/{6000}, Loss: {loss.item():.4f}")
#     torch.save(model.state_dict(), "model.pth")



def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    #s_words = [stemmer.stem(word.lower()) for word in words]
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    for str in s_words:
        for i,w in enumerate(words):
            if w==str:
                bag[i] = (1)
    return np.array(bag)
def text_to_str():
    recognizer = speech_recognition.Recognizer()
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=1)
            audio = recognizer.listen(mic)
            text = recognizer.recognize_google(audio)
            text = text.lower()
            #print(text)
            # assistant.request(text)
    except:
        recognizer = speech_recognition.Recognizer()
        pass

def check_responses(text, tag):
    for tg in data["intents"]:
        if tg["tag"] == tag:
            responses = tg["responses"]  # TODO
            if tag == "time":
                current_time = datetime.datetime.now()
                current_time = current_time.strftime("%I:%M:%S %p")
                responses = ["The current time Is: ", "The time is: ", "It is currently: "]
                responses = [resp + str(current_time) for resp in responses]
                predictions = rn.choice(responses)
                bot_talk(predictions)
            # elif (tag == "time_other"):
            #     i = -1
            #     loc = text.split(" ")
            #     countries = list(pycountry.countries())
            #     for country in countries:
            #         for words in loc:
            #             if (country.lower() == words.lower()):
            #                 given_country = country
            #         given_country = ""
            #     if (given_country == ""):
            #         current_time = datetime.datetime.now()
            #         current_time = current_time.strftime("%I:%M:%S %p")
            #         responses = [f"The time at your location is: {current_time}"]
            #     else:
            #         tz = pytz.country_timezones(given_country)[0]
            #         current_time = datetime.datetime.now(pytz.timezone(tz))
            #         current_time = current_time.strftime("%I:%M:%S %p")
            #         responses = [f"The time at {given_country} is: {current_time}"]
            elif tag == "weather":
                # get your current location using your IP address
                response = requests.get('https://ipapi.co/json/')
                location_data = response.json()

                # get the weather at your current location using the OpenWeatherMap API
                api_key = 'b7e17f2484b3ef4f4d718674816f1876'
                url = f'https://api.openweathermap.org/data/2.5/weather?lat={location_data["latitude"]}&lon={location_data["longitude"]}&appid={api_key}&units=metric'
                response = requests.get(url)
                weather_data = response.json()
                responses = [f'The weather at your current location ({location_data["city"]}, {location_data["country"]}) is {weather_data["weather"][0]["description"]}. The temperature is {weather_data["main"]["temp"]} degrees Celsius.']
                predictions = rn.choice(responses)
                bot_talk(predictions)
            elif tag == "news":
                # set the RSS feed URL for Google News
                url = 'https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en'
                # parse the RSS feed and get the latest news
                feed = feedparser.parse(url)
                for entry in feed.entries:
                    title = re.sub(r'<[^>]+>', '', entry.title)
                    description = re.sub(r'<[^>]+>', '', entry.description)
                    description = re.sub(r"&nbsp", ' ', description)
                    responses = [title + " " + description[:1000]]

                predictions = rn.choice(responses)
                bot_talk(predictions)
            elif tag == "play_music" or tag == "music":
                search_query = text.lower().replace("play", "")
                pywhatkit.playonyt(search_query)
                responses = [f"Here is {search_query} On Youtube"]
                predictions = rn.choice(responses)
                bot_talk(predictions)
            elif tag == "search":
                search_query = text.lower().replace("find", "")
                search_query = search_query.lower().replace("search", "")
                search_query = search_query.lower().replace("for", "")
                search_query = search_query.lower().replace("please", "")
                search_query = search_query.lower().replace("about", "")
                search_query = search_query.lower().replace("could", "")
                search_query = search_query.lower().replace("google", "")
                url = f"https://www.google.com/search?q={search_query}"
                query_data = googlesearcher.Google.search(search_query, num = "1")
                print(query_data)
                responses = [response.title for response in query_data]
                predictions = rn.choice(responses)
                bot_talk(predictions)
                webbrowser.open_new_tab(url)
                # bot_talk("Would You Like To Open A Web Browser?")
                # try:
                #     with speech_recognition.Microphone() as mic:
                #         recognizer.adjust_for_ambient_noise(mic, duration=1)
                #         audio = recognizer.listen(mic)
                #         text = recognizer.recognize_google(audio)
                #         text = text.lower()
                #         if "yes" in text:
                #             webbrowser.open_new_tab(url)
                #             break
                #         elif "no" in text:
                #             return
                # except:
                #     break



def reply():
    Cont = True
    engine.say("Hi, Welcome To The Bearcat ChatBot. And I am YUCY Voice Assistant!")
    print("Hi, Welcome To The Bearcat ChatBot. And I am YUCY Voice Assistant!")
    engine.say("How Can I Help You?      You May Say Quit or Stop at anytime to end the conversation!")
    print("How Can I Help You?\nYou May Say Quit or Stop at anytime to end the conversation!")
    engine.runAndWait()
    while Cont:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=1)
                audio = recognizer.listen(mic)
                text = recognizer.recognize_google(audio)
                text = text.lower()
                print(text)
                our_reply = model.predict([bag_of_words(text, words)])
                #print(our_reply)
                if (text == "quit" or text == "stop"):
                    quit()
                    break
                predictions = model.predict([bag_of_words(text, words)])[0]
                #print(predictions)
                predictions_index = np.argmax(predictions)
                tag = labels[predictions_index]
                check_responses(text, tag)
                #print(tag)
                # if (predictions[predictions_index] > 0.4):
                #     tag = labels[predictions_index]
                #     check_responses(text, tag)
                # else:
                #     for tg in data["intents"]:
                #         if tg["tag"] == "random_replies":
                #             responses = tg["responses"] #TODO
                #     predictions = rn.choice(responses)
                #     bot_talk(predictions)

                #bot_reply(text)
                #assistant.request(text)
        except:
            recognizer = speech_recognition.Recognizer()
            pass

reply()
# assistant = GenericAssistant('intents.json', intent_methods=mappings, model_name="test_model")
# assistant.train_model()
# assistant.save_model()

# def bot_reply(command):
#     #assitant.request(command)
#     command = command.lower()
#     print(command)
#     bot_talk(command)
#     if (command == "stop" or command == "bye" or command == "end" or command == 'goodbye' or command == "good bye"):
#         global Cont
#         Cont = False
#         bot_talk("It was nice talking to you!")
#         bot_talk("Hope you have a great day ahead!")
#     if (command == "where is tuc"):
#         bot_talk("TUC - Tangamin University Center is close by")
#     words = command.split(" ")

'''
  {"tag": "travel",
    "patterns": ["What's your favorite travel destination?", "Can you recommend a good place to visit?", "What's the best time to travel?", "How do I get to [place]?"],
    "responses": ["I don't have a favorite travel destination, since I don't go on trips!", "Have you considered visiting [place]? I've heard it's really nice!", "The best time to travel depends on the place you're going to and your preferences!", "To get to [place], you can take a [mode of transportation], did that help?"],
    "context_set": ""
  },
    {"tag": "stocks",
    "patterns": ["what stocks do I own?", "how are my shares?", "what companies am I investing in?", "what am I doing in the markets?"],
    "responses": ["I do not have any information about your stocks!"],
    "context_set": ""
  },
    {
    "tag": "time_random",
    "patterns": ["is your favorite time of the day?", "Do you have any time management tips?", "Can you tell me a fun fact about time?"],
    "responses": ["I don't have a favorite time of the day since I'm an AI.", "Sure, some time management tips include prioritizing tasks and breaking them down into smaller ones.", "Did you know that time dilation occurs in space? Time passes slower in stronger gravitational fields."],
    "context_set": ""
  },
'''

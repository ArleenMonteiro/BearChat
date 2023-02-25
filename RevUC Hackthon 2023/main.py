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
import datetime
import wikipedia as wp
import webbrowser
import time
import subprocess
import ecapture as ec
import wolframalpha as wra
import sys
import os
import pycountry
import pytz
import requests
import feedparser
import re


stemmer = LancasterStemmer()
Cont = True
recognizer = speech_recognition.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 145)

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

    # Starting the tensorflow modelling
    #tensorflow.reset_default_graph()
tensorflow.compat.v1.reset_default_graph()

net = tfl.input_data(shape=[None, len(training[0])])
net = tfl.fully_connected(net, 8)
net = tfl.fully_connected(net, 8)
net = tfl.fully_connected(net, len(output[0]), activation="softmax")
net = tfl.regression(net)

model = tfl.DNN(net)

try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=15000, batch_size=8, show_metric=True)
    model.save("model.tflearn")
    #net = tfl.fully_connected(net, 8)


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

def check_responses(text, tag):
    for tg in data["intents"]:
        if tg["tag"] == tag:
            responses = tg["responses"]  # TODO
            if tag == "time":
                current_time = datetime.datetime.now()
                current_time = current_time.strftime("%I:%M:%S %p")
                responses = ["The current time Is: ", "The time is: ", "It is currently: "]
                responses = [resp + str(current_time) for resp in responses]
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
            elif tag == "news":
                # set the RSS feed URL for Google News
                url = 'https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en'
                # parse the RSS feed and get the latest news
                feed = feedparser.parse(url)
                for entry in feed.entries:
                    title = re.sub(r'<[^>]+>', '', entry.title)
                    description = re.sub(r'<[^>]+>', '', entry.description)
                    description = re.sub(r"&nbsp", ' ', description)
                    print(description)
                    responses = [title + " " + description]
    predictions = rn.choice(responses)
    bot_talk(predictions)

def reply():
    Cont = True
    # engine.say("Hi, This is The Bearcat ChatBot")
    # print("Hi, This is The Bearcat ChatBot")
    # engine.say("How Can I Help You?      You May Say Quit or Stop at anytime to end the conversation!")
    # print("How Can I Help You?\nYou May Say Quit or Stop at anytime to end the conversation!")
    # engine.runAndWait()
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

                # else:
                #     for tg in data["intents"]:
                #         if tg["tag"] == "random_replies":
                #             responses = tg["responses"] #TODO
                #     predictions = rn.choice(responses)
                #     bot_talk(predictions)

                # bot_reply(text)
                # assistant.request(text)
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
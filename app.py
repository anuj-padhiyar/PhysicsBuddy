from flask import Flask, render_template, request, jsonify
import nltk
import pickle
import numpy as np
from keras.models import load_model
import json
import random

custom_data_path = "./nltk_data"
nltk.data.path.append(custom_data_path)
nltk.download('punkt', download_dir=custom_data_path)
nltk.download('wordnet', download_dir=custom_data_path)

lemmatizer = nltk.stem.WordNetLemmatizer()
model = load_model('./files/chatbot_model.h5')
data = json.loads(open('./files/data.json').read())
words = pickle.load(open('./files/words.pkl','rb'))
classes = pickle.load(open('./files/classes.pkl','rb'))


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    return get_Chat_response(msg)

def get_Chat_response(text):
    text = text.lower()
    if text in ["how are you"]:
        response = "I'm doing well, thank you. How about you?"
    elif text in ["what's your name", "your name"]:
        response = "I am a chatbot created by stackfire. You can call me PhysicsBuddy."
    elif text in ["hello", "hi", "hey"]:
        response = "Hi there, I am PhysicsBuddy."
    elif text in ["weather today", "how's the weather", "what is the weather like", "weather"]:
        response = "I'm sorry, I'm an chatbot and don't have access to real-time data."
    elif text in ["where are you from", "your location"]:
        response = "I exist in the digital world and don't have a physical presence, so I don't have a specific location. But I'm here to assist you!"
    elif text in ["how old are you", "your age"]:
        response = "As an chatbot, I don't have an age or personal information. My purpose is to assist and provide useful information."
    elif text in ["your hobbies", "what do you do for fun","hobbies","hobby"]:
        response = "Since I'm an chatbot, I don't have hobbies, but I enjoy helping users like you with information and answering question."
    elif text in ["bye","good bye","take care","see you"]:
        response = "Good Bye Have a nice day"
    else:
        response = chatbot_response(text)
    return response

def chatbot_response(text):
    ints = predict_class(text, model)
    if len(ints):
        return getResponse(ints, data)
    return "I'm sorry, I couldn't understand your question. Could you please rephrase it?"
    
def getResponse(ints, intents_json):
    tag = ints[0]['id']
    list_of_intents = intents_json['data']
    for i in list_of_intents:
        if(i['id']== tag):
            result = i['answer']
            break
    return result

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"id": classes[r[0]], "probability": str(r[1])})
    return return_list

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)

    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)

    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    csentence_words = convert_numbers(sentence_words);
    return sentence_words

def convert_numbers(words):
    ordinal = {'first':'1','second':'2','third':'3'}
    for word in words:
        if word in ordinal.keys():
            words.extend(ordinal[word])
    return words

if __name__ == '__main__':
    app.run()
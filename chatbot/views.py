import json
import random
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

############# chatbot-neural network

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())


classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    words = pickle.load(open('words.pkl', 'rb'))
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRUSHOLD = 0.25
    results = [[i,r] for i, r in enumerate(res) if r > ERROR_THRUSHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result


class ChatQuery(APIView):
    
    def post(self, request):
        data = json.load(request)
        query = data["query"]
        ints = predict_class(query)
        res = get_response(ints, intents)

        return Response(
                {
                    "val": "Response sent",
                    "data": res
                }, status=status.HTTP_200_OK)

import re
import json
import random
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# # Create your views here.

# def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
#     message_certainty = 0
#     has_required_words = True

#     for word in user_message:
#         if word in recognised_words:
#             message_certainty += 1
    
#     percentage = float(message_certainty) / float(len(recognised_words))

#     for word in required_words:
#         if word not in user_message:
#             has_required_words = False
#             break
    
#     if has_required_words or single_response:
#         return int(percentage*100)
#     else:
#         return 0


# def check_all_messages(message):
#     highest_prob_list = {}

#     def response(bot_response, list_of_words, single_response=False, required_words=[]):
#         highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

#     #Responses ----------------------------------------------
#     response('Hello!', ['hello', 'hi', 'sup', 'hey', 'heyo', 'heyy', 'heyyy', 'hii', 'hiii', 'hiiii', 'hola', 'holaa', 'wassup', 'hiee'], single_response=True)
#     response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
#     response('Thank you!', ['i', 'love', 'this', 'site'], required_words=['this', 'site'])
#     response('''Procurement by Public organizations like- Ministries, Banks, Defense, Federal Government, State Government, Municipal Corporations, Counties etc for the benefit of public and from the public fund is know as Public Procurement.''', ['what', 'is', 'public', 'procurement'], required_words=['what', 'procurement'])
#     response('''No, you can not. If you at all wish to then you have to forfeit your EMD''', ['can', 'i', 'withdraw', 'a', 'bid'], required_words=['withdraw', 'bid'])
#     response('''BG is a mode of taking EMD. It is prefered for higher amount.''', ['what', 'is', 'BG'], required_words=['BG'])
#     response('''The bidder can’t do much. In certain cases the tendering authority allow the bidder to withdraw their bid.''', ['what', 'to', 'do', 'when', 'tender', 'is', 'BG'], required_words=['do', 'tender'])
#     response('''The delay can be on account of poor response, certain modifications/amendments in the bid terms and conditions etc.''', ['why', 'is', 'tender', 'delayed'], required_words=['why', 'tender'])
#     response('''For any query requiring urgent assistance, contact tollfree number: 1234567890, 0987654321. Email support: email.support@email.com''', ['can\'t', 'resolve', 'query', 'customer', 'care'], required_words=['customer', 'care'])
    
#     # Navigation
#     # response('')

#     best_match = max(highest_prob_list, key=highest_prob_list.get)
#     # print(highest_prob_list)

#     return unkown() if highest_prob_list[best_match] < 1 else best_match

# def get_response(user_input):
#     split_message = re.split(r'\s+|[,;?!\'.-]\s*', user_input.lower())
#     response = check_all_messages(split_message)
#     return response


# def unkown():
#     response = ['Could you please re-phrase that?',
#                 "...",
#                 "Sounds about right",
#                 "What does that mean?",
#                 "I am unable to understand. Sorry",
#                 "Can you please use simplar words"][random.randrange(6)]
    
#     return response

# class ChatQuery(APIView):
    
#     def post(self, request):
#         data = json.load(request)

#         query = data["query"]

#         resp = get_response(query)
        
#         return Response(
#                 {
#                     "val": "Response sent",
#                     "data": resp
#                 }, status=status.HTTP_200_OK)
        
# while True:
#     print('Bot: '+ get_response(input('You: ')))


############# chatbot-neural network

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())


classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.model')

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

        # resp = get_response(query)
        
        return Response(
                {
                    "val": "Response sent",
                    "data": res
                }, status=status.HTTP_200_OK)

# while True:
#     words = pickle.load(open('words.pkl', 'rb'))
#     message = input("")
#     ints = predict_class(message)
#     res = get_response(ints, intents)
#     print(res)
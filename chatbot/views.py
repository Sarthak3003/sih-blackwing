import  re
import json
import random
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognised_words:
            message_certainty += 1
    
    percentage = float(message_certainty) / float(len(recognised_words))

    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break
    
    if has_required_words or single_response:
        return int(percentage*100)
    else:
        return 0


def check_all_messages(message):
    highest_prob_list = {}

    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    #Responses ----------------------------------------------
    response('Hello!', ['hello', 'hi', 'sup', 'hey', 'heyo'], single_response=True)
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('Thank you!', ['i', 'love', 'this', 'site'], required_words=['this', 'site'])
    
    # Navigation
    # response('')

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    # print(highest_prob_list)

    return unkown() if highest_prob_list[best_match] < 1 else best_match

def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!\'.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response


def unkown():
    response = ['Could you please re-phrase that?', "...", "Sounds about right", "What does that mean?"][random.randrange(4)]
    
    return response

class ChatQuery(APIView):
    
    def post(self, request):
        data = json.load(request)

        query = data["query"]

        resp = get_response(query)
        
        return Response(
                {
                    "val": "Response sent",
                    "data": resp
                }, status=status.HTTP_200_OK)
        
# while True:
#     print('Bot: '+ get_response(input('You: ')))
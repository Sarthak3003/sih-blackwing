import  re
import json
import random
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class BestBid(APIView):

    def post(self, request):
        data  = json.load(request)
        points = 0

        '''
        bider id: something waisa
        quantity: number of units
        units: kg/ml/L/...
        Preffered Brand: brand names
        Offered Brand: brand names
        Expected price: number
        Offered prive: number
        Total: pura price
        '''
        print(data)
        pref_model_list = []
        off_model_list = []

        for i in data['pref_model']:
            print(i)
            if i in off_model_list:
                point +=1
            # pref_model_list.append(i)
        
        print(pref_model_list)

        
        return Response(
                {
                    "val": "Response sent",
                    "data": data
                }, status=status.HTTP_200_OK)

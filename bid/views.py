import  re
import csv
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
        point = 0

        pref_model_list = {}
        off_model_list = {}

        requirement = data['requirement']
        response = data['response']
        response = response[0]
        id = response['bidder id']
        print(len(requirement))


        for item in requirement:
            sl = item['sl no']
            # for i in item['pref_model']:
            #     l1.append(i)
            pref_model_list[sl] = item['pref_model']
            
            
        for item in response['bidder offer']:
            sl = item['sl no']
            # for i in item['offered_model']:
            #     l2.append(i)

            off_model_list[sl] = item['offered_model']

        print(pref_model_list)
        print(off_model_list)

        for i in pref_model_list:
            if i in off_model_list:
                point +=1
            # pref_model_list.append(i)
            print(point)

        




        
        return Response(
                {
                    "val": "Response sent",
                    "data": data
                }, status=status.HTTP_200_OK)


















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

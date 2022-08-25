import  re
import csv
import json
import random
import itertools
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class BestBid(APIView):

    def post(self, request):
        data  = json.load(request)
        point_data = {}
        # point = 0

        pref_model_list = {}
        off_model_list = {}

        requirement = data['requirement']

        for item in requirement:
            sl = item['sl no']
            pref_model_list[sl] = item['prefered models']

        # print(pref_model_list)

        response = data['response']
        print("Total bids are: ", len(response))
        # print(response)
        for re in range(len(response)):
            
            resp = response[re]
            i = 1
            k = 0
            point = 0
            id = resp['bidder id']
            for item in resp['bidder offer']:
                sl = item['sl no']
                off_model_list[sl] = item['offered models']

            while i <= len(pref_model_list):
                for j in pref_model_list[str(i)]:
                    if j in off_model_list[str(i)]:
                        point +=1
                i += 1
            k += 1
            point_data[id] = point

        print(point_data)

        print("Top 5 bids we rec are: ")

        data_dict = dict(sorted(point_data.items(), key=lambda item: item[1], reverse=True))
        data_dict = dict(itertools.islice(data_dict.items(),3))
        print(data_dict)






        




        
        return Response(
                {
                    "val": "Response sent",
                    "data": data_dict
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

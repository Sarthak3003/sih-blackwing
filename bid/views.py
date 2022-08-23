import  re
import json
import random
from socketserver import ForkingMixIn
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class BestBid(APIView):

    def post(self, request):
        data  = json.load(request)

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
        
        return Response(
                {
                    "val": "Response sent",
                    "data": data
                }, status=status.HTTP_200_OK)

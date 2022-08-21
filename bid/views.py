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
        
        return Response(
                {
                    "val": "Response sent",
                    "data": data
                }, status=status.HTTP_200_OK)

import json
import itertools
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class BestBid(APIView):

    def post(self, request):
        data  = json.load(request)
        point_data = {}

        pref_model_list = {}
        off_model_list = {}
        expect_rate = {}
        offered_rate = {}

        requirement = data['requirement']

        for item in requirement:
            sl = item['sl no']
            pref_model_list[sl] = item['prefered models']
            expect_rate[sl] = item['Estimated Rate']

        response = data['response']
        print("Total bids are: ", len(response))
        
        for re in range(len(response)):
            resp = response[re]
            i = 1
            mod_point = 0
            rate_point = 0
            id = resp['bidder id']

            #### Prefered and Offered Models Point Scheme

            for item in resp['bidder offer']:
                sl = item['sl no']
                off_model_list[sl] = item['offered models']
                offered_rate[sl] = item['unit rate']

            while i <= len(pref_model_list):
                for j in pref_model_list[str(i)]:
                    if j in off_model_list[str(i)]:
                        mod_point +=1
                i += 1

            point_data[id] = mod_point

            #### Prefered and Offered Models Point Scheme

            i = 0

            while i < len(expect_rate):
                j = expect_rate[str(i+1)]
                if j > offered_rate[str(i+1)]:
                    rate_point += 1
                elif j == offered_rate[str(i+1)]:
                    rate_point += 0
                else:
                    rate_point -= 1
                i += 1

            point_data[id] += rate_point

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
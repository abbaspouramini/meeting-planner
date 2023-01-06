import datetime

from django.http import JsonResponse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .serializers import *
from .models import Meeting, OwnerAvailableTimes
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.http import JsonResponse

# Create your views here.
class MeetingApi(APIView):
    def post(self,request):
        serializer = MeetingSerializer(data=request.data)
        token=request.headers["Authorization"][6:]
        owner=User.objects.get(id=Token.objects.get(key=token).user_id)
        if serializer.is_valid():
            serializer.validated_data["ownerID"]=owner
            data = serializer.save()
            id = data.id
            return Response({
                'id': id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class MeetEditApi(APIView):
    def get(self,request,meetid):
        try:
            meeting = Meeting.objects.get(pk=meetid)
        except Meeting.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MeetingSerializer(meeting)
        return Response(serializer.data)

    def put(self,request,meetid):
        try:
            meeting = Meeting.objects.get(pk=meetid)
        except Meeting.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MeetingSerializer(meeting,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class OwnerTimeApi(APIView):
    def post(self, request,meetid):
        meet=Meeting.objects.get(id=meetid)
        records=OwnerAvailableTimes.objects.filter(meetID=meet)
        records.delete()
        for i in request.data['Times']:
            serializer=MeetingTimeSerializer(data=i)
            if serializer.is_valid():
                serializer.validated_data["meetID"]=meet
                serializer.save()
                if i==request.data["Times"][-1]:
                    return JsonResponse(request.data,status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class EditTimeApi(OwnerTimeApi):
    def get(self,request,meetid):
        try:
            meet = Meeting.objects.get(id=meetid)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        records = OwnerAvailableTimes.objects.filter(meetID=meet)
        OutResponse={
            'Sat':[],
            'Sun':[],
            'Mon':[],
            'Tue':[],
            'Wen':[],
            'Thu':[],
            'Fri':[]
        }
        for object in records:
            OutResponse[object.day].append({'startTime':object.startTime,'endTime':object.endTime})

        return JsonResponse(OutResponse,status=status.HTTP_200_OK)


class InvitationLinkApi(APIView):

    def get(self,request,meeturl):
        try:
            meet=Meeting.objects.get(url=meeturl)
        except Meeting.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        result= {"Sat":[],
                 "Sun":[],
                 "Mon":[],
                 "Tue":[],
                 "Thu":[],
                 "Wen":[],
                 "Fri":[],
                 "duration":meet.duration}

        records = OwnerAvailableTimes.objects.filter(meetID=meet)
        for i in records:
                stime = datetime.datetime.combine(datetime.date(1, 1, 1), i.startTime)
                etime = datetime.datetime.combine(datetime.date(1, 1, 1), i.endTime)
                d = str(meet.duration).split(":")
                duration = datetime.timedelta(hours=int(d[0]),minutes=int(d[1]))
                delta= datetime.timedelta(hours=0,minutes=30)
                curtime = stime
                while (curtime + duration < etime):
                    result[i.day].append(str(curtime.time()))
                    curtime = curtime + delta
        return JsonResponse(result)




class CheckURL(APIView):
    def post(self,request):
        existedmeet=Meeting.objects.filter(url=request.data['url'])
        if len(existedmeet)>0:
            return JsonResponse({"URL_isuniqe":False},status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({"URL_isuniqe":True},status=status.HTTP_202_ACCEPTED)

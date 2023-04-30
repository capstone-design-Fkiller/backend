from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from locker.models import Locker
from locker.serializers import LockerSerializer, LockerMajorSerializer

class LockerAPIView(APIView):
    def get(self, request):
        lockers = Locker.objects.all()

        serializer = LockerSerializer(lockers, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = LockerSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LockerDetail(APIView):
    def get_object(self, pk):
        try:
            return Locker.objects.get(pk=pk)
        except Locker.DoesNotExist:
            raise Http404
    
    # User의 detail 보기
    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = LockerSerializer(user)
        return Response(serializer.data)

    # User 수정하기
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = LockerSerializer(user, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # User 삭제하기
    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class LockerMajor(APIView):
    def get_queryset(self):
        return Locker.objects.filter(major__id="1")
    
    # LockerMajor 조회하기
    def get(self, request, format=None):
        locker_major = self.get_queryset()
        serializer = LockerMajorSerializer(locker_major, many=True)
        return Response(serializer.data)

    # UserMajor 수정하기
    def put(self, request, format=None):
        locker_major = self.get_queryset()
        serializer = LockerMajorSerializer(locker_major, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # UserMajor 삭제하기
    def delete(self, request, format=None):
        locker_major = self.get_queryset()
        locker_major.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from user.models import User
from user.serializers import UserPostSerializer, UserSerializer, UserMajorSerializer

class UserAPIView(APIView):
    def get(self, request):
        users = User.objects.all()

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = UserPostSerializer(data = request.data)
        # serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    
    # User의 detail 보기
    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    # User 수정하기
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # User 삭제하기
    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class UserMajor(APIView):
    def get_queryset(self):
        return User.objects.filter(major__id="1")
    
    # UserMajor 조회하기
    def get(self, request, format=None):
        user_major = self.get_queryset()
        serializer = UserMajorSerializer(user_major, many=True)
        return Response(serializer.data)

    # UserMajor 수정하기
    def put(self, request, format=None):
        user_major = self.get_queryset()
        serializer = UserMajorSerializer(user_major, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # UserMajor 삭제하기
    def delete(self, request, format=None):
        user_major = self.get_queryset()
        user_major.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
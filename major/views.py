from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from major.models import Major
from major.serializers import MajorSerializer

class MajorAPIView(APIView):
    def get(self, request):
        users = Major.objects.all()

        serializer = MajorSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = MajorSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MajorDetail(APIView):
    def get_object(self, pk):
        try:
            return Major.objects.get(pk=pk)
        except Major.DoesNotExist:
            raise Http404
    
    # Blog의 detail 보기
    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = MajorSerializer(user)
        return Response(serializer.data)

    # Blog 수정하기
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = MajorSerializer(user, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Blog 삭제하기
    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from major.models import Major
from major.serializers import MajorSerializer

class MajorAPIView(APIView):
    def get(self, request):
        majors = Major.objects.all()

        serializer = MajorSerializer(majors, many=True)
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
    
    # Major의 detail 보기
    def get(self, request, pk, format=None):
        major = self.get_object(pk)
        serializer = MajorSerializer(major)
        return Response(serializer.data)

    # Major 수정하기
    def put(self, request, pk, format=None):
        major = self.get_object(pk)
        serializer = MajorSerializer(major, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Major 삭제하기
    def delete(self, request, pk, format=None):
        major = self.get_object(pk)
        major.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
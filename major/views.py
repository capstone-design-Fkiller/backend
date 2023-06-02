from django.forms import ValidationError
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from major.models import Major
from major.serializers import MajorSerializer, MajorRequestSerializer

class MajorAPIView(generics.ListCreateAPIView):
    serializer_class = MajorSerializer
    queryset = Major.objects.all()

    def get(self, request, **kwargs):
        try:
            if request.GET: # 쿼리 존재시, 쿼리로 필터링한 데이터 전송.
                params = request.GET
                params = {key: (lambda x: params.get(key))(value) for key, value in params.items()}
                majors = Major.objects.filter(**params)
            else: # 쿼리 없을 시, 전체 데이터 요청
                majors = Major.objects.all()

            serializer = MajorSerializer(majors, many=True)
            return Response(serializer.data)
        except ValidationError as err:
                return Response({'detail': f'{err}'}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        serializer = MajorSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MajorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Major.objects.all()
    serializer_class = MajorRequestSerializer
    
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
    
    
    def patch(self, request, pk, format=None):
        major = self.get_object(pk)
        serializer = MajorRequestSerializer(major, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Major 수정하기
    def put(self, request, pk, format=None):
        major = self.get_object(pk)
        serializer = MajorRequestSerializer(major, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Major 삭제하기
    def delete(self, request, pk, format=None):
        major = self.get_object(pk)
        major.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
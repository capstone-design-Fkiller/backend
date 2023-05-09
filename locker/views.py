from django.forms import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from locker.models import Locker
from locker.serializers import LockerSerializer, LockerPostSerializer

class LockerAPIView(APIView):
    def get(self, request, **kwargs):
        try:
            if request.GET: # 쿼리 존재시, 쿼리로 필터링한 데이터 전송.
                params = request.GET
                params = {key: (lambda x: params.get(key))(value) for key, value in params.items()}
                lockers = Locker.objects.filter(**params)
            else: # 쿼리 없을 시, 전체 데이터 요청
                lockers = Locker.objects.all()

            serializer = LockerSerializer(lockers, many=True)
            return Response(serializer.data)
        except ValidationError as err:
                return Response({'detail': f'{err}'}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        serializer = LockerPostSerializer(data = request.data)
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
    
    # Locker의 detail 보기
    def get(self, request, pk, format=None):
        locker = self.get_object(pk)
        serializer = LockerSerializer(locker)
        return Response(serializer.data)

    # Locker 수정하기
    def put(self, request, pk, format=None):
        locker = self.get_object(pk)
        serializer = LockerSerializer(locker, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Locker 삭제하기
    def delete(self, request, pk, format=None):
        locker = self.get_object(pk)
        locker.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
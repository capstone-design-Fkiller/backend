from django.forms import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from alert.models import Alert  
from alert.serializers import AlertSerializer

class AlertView(APIView):
    def get(self, request):
        try:
            if request.GET: # 쿼리 존재시, 쿼리로 필터링한 데이터 전송.
                params = request.GET
                params = {key: (lambda x: params.get(key))(value) for key, value in params.items()}
                applys = Alert.objects.filter(**params)
            else: # 쿼리 없을 시, 전체 데이터 요청
                applys = Alert.objects.all()
            serializer = AlertSerializer(applys, many=True)
            return Response(serializer.data)
        except ValidationError as err:
                return Response({'detail': f'{err}'}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        serializer = AlertSerializer(data = request.data) # json을 변환하게 된다.
        if serializer.is_valid():
            alert = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AlertDetail(APIView):
    def get_object(self, pk):
        try:
            return Alert.objects.get(pk=pk)
        except Alert.DoesNotExist:
            raise Http404
    
    # alert의 detail 보기
    def get(self, request, pk, format=None):
        alert = self.get_object(pk)
        serializer = AlertSerializer(alert)
        return Response(serializer.data)

    # alert 수정하기
    def put(self, request, pk, format=None):
        alert = self.get_object(pk)
        serializer = AlertSerializer(alert, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # alert 삭제하기
    def delete(self, request, pk, format=None):
        alert = self.get_object(pk)
        Alert.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
from django.forms import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from alert.models import Alert  
from alert.serializers import AlertPatchSerializer, AlertPostSerializer, AlertSerializer
# from rest_framework import viewsets
from rest_framework import generics


class AlertView(generics.ListCreateAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer

    def get(self, request):
        try:
            if request.GET: # 쿼리 존재시, 쿼리로 필터링한 데이터 전송.
                params = request.GET
                params = {key: (lambda x: params.get(key))(value) for key, value in params.items()}
                alerts = Alert.objects.filter(**params)
            else: # 쿼리 없을 시, 전체 데이터 요청
                alerts = Alert.objects.all()
            serializer = AlertSerializer(alerts, many=True)
            return Response(serializer.data)
        except ValidationError as err:
                return Response({'detail': f'{err}'}, status=status.HTTP_400_BAD_REQUEST)
    
    # 알림 전송 --- 관리자가 사용자를 지정할 때 receiver = 17
    def post(self, request):
        serializer = AlertPostSerializer(data = request.data)
        if serializer.is_valid():
            alert = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        alerts = Alert.objects.all()
        alerts.delete()
        print("알림 삭제 완료")
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class AlertDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AlertSerializer

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
    def patch(self, request, pk, format=None):
        alert = self.get_object(pk)
        serializer = AlertSerializer(alert, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    

class AlertConvertIsRead(generics.RetrieveUpdateAPIView):
    serializer_class = AlertPatchSerializer
    queryset = Alert.objects.all()

    def get(self, request, receiver):
        try:
            if request.GET: # 쿼리 존재시, 쿼리로 필터링한 데이터 전송.
                params = request.GET
                params = {key: (lambda x: params.get(key))(value) for key, value in params.items()}
                alerts = Alert.objects.filter(**params)
            else: # 쿼리 없을 시, 전체 데이터 요청
                alerts = Alert.objects.all()
            serializer = AlertSerializer(alerts, many=True)
            return Response(serializer.data)
        except ValidationError as err:
                return Response({'detail': f'{err}'}, status=status.HTTP_400_BAD_REQUEST)

    # alert 읽음 여부 수정하기
    def patch(self, request, receiver, format=None):
        try:
            # receiver의 알림들
            alerts = Alert.objects.filter(receiver=receiver)

            for alert in alerts:
                if alert.isRead == False: # receiver의 alerts 중 isRead가 False인 아직 읽지 않은 게 있다면,
                    alert.isRead = True  # 모두 읽음으로 변경.
                    alert.save()
            serializer = AlertSerializer(alerts, many=True)
            return Response(serializer.data) 
        except Exception as err:
            return Response({'detail': f'{err}'}, status=status.HTTP_400_BAD_REQUEST)
    
    # alert 읽음 여부 수정하기
    def put(self, request, receiver, format=None):
        try:
            # receiver의 알림들
            alerts = Alert.objects.filter(receiver=receiver)

            for alert in alerts:
                if alert.isRead == False: # receiver의 alerts 중 isRead가 False인 아직 읽지 않은 게 있다면,
                    alert.isRead = True  # 읽음으로 변경.
                    alert.save()
            serializer = AlertSerializer(alerts, many=True)
            return Response(serializer.data) 
        except Exception as err:
            return Response({'detail': f'{err}'}, status=status.HTTP_400_BAD_REQUEST)
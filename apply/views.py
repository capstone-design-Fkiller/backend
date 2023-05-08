from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from apply.models import Apply, Priority1
from apply.serializers import ApplySerializer, PrioritySerializer

class PriorityAPIView(APIView):
    def get(self, request):
        priorities = Priority1.objects.all()
        serializer = PrioritySerializer(priorities, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = PrioritySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 유효성 검사 실패 시 예외 발생
        serializer.save()  # serializer를 통해 데이터를 모델 인스턴스로 저장
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ApplyAPIView(APIView):
    def get(self, request):
        applys = Apply.objects.all()

        serializer = ApplySerializer(applys, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ApplySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ApplyDetail(APIView):
    def get_object(self, pk):
        try:
            return Apply.objects.get(pk=pk)
        except Apply.DoesNotExist:
            raise Http404
    
    # Apply의 detail 보기
    def get(self, request, pk, format=None):
        apply = self.get_object(pk)
        serializer = ApplySerializer(apply)
        return Response(serializer.data)

    # Apply 수정하기
    def put(self, request, pk, format=None):
        apply = self.get_object(pk)
        serializer = ApplySerializer(apply, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Apply 삭제하기
    def delete(self, request, pk, format=None):
        apply = self.get_object(pk)
        apply.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
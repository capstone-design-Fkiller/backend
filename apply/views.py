from django.forms import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from apply.models import Apply, Priority1, Priority2, Priority3
from apply.serializers import ApplySerializer, PrioritySerializer

class PriorityAPIView(APIView):
    def get(self, request):
        try:
            if request.GET: # 쿼리 존재시, 쿼리로 필터링한 데이터 전송.
                params = request.GET
                params = {key: (lambda x: params.get(key))(value) for key, value in params.items()}
                priorities = Priority1.objects.filter(**params)
            else: # 쿼리 없을 시, 전체 데이터 요청
                priorities = Priority1.objects.all()
            serializer = PrioritySerializer(priorities, many=True)
            return Response(serializer.data)
        except ValidationError as err:
                return Response({'detail': f'{err}'}, status=status.HTTP_400_BAD_REQUEST)
    
    # def post(self, request, format=None):
    #     serializer = PrioritySerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)  # 유효성 검사 실패 시 예외 발생
    #     serializer.save()  # serializer를 통해 데이터를 모델 인스턴스로 저장
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

class ApplyAPIView(APIView):
    def get(self, request):
        try:
            if request.GET: # 쿼리 존재시, 쿼리로 필터링한 데이터 전송.
                params = request.GET
                params = {key: (lambda x: params.get(key))(value) for key, value in params.items()}
                applys = Apply.objects.filter(**params)
            else: # 쿼리 없을 시, 전체 데이터 요청
                applys = Apply.objects.all()
            serializer = ApplySerializer(applys, many=True)
            return Response(serializer.data)
        except ValidationError as err:
                return Response({'detail': f'{err}'}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        serializer = ApplySerializer(data = request.data) # json을 변환하게 된다.
        if serializer.is_valid():
            apply = serializer.save()
            priority_1_answer = serializer.validated_data.get("priority_1_answer")
            priority_2_answer = serializer.validated_data.get("priority_2_answer")
            priority_3_answer = serializer.validated_data.get("priority_3_answer")
            if priority_1_answer:
                priority1 = Priority1.objects.create(question=serializer.validated_data['major'], answer=apply)
                priority1.save()
            if priority_2_answer:
                priority2 = Priority2.objects.create(question=serializer.validated_data['major'], answer=apply)
                priority2.save()
            if priority_3_answer:
                priority3 = Priority3.objects.create(question=serializer.validated_data['major'], answer=apply)
                priority3.save()
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
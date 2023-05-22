from django.forms import ValidationError
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django.http import Http404
from django.core.management import call_command
from django.db.models.functions import RowNumber
from django.db.models import Count, F, Window

from apply.models import Apply
from major.models import Major
from apply.serializers import ApplySerializer, ApplyPostSerializer, SortSerializer

class ApplyAPIView(generics.ListCreateAPIView):
    def get(self, request, **kwargs):
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
        serializer = ApplyPostSerializer(data = request.data) # json을 변환하게 된다.
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ApplyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Apply.objects.all()
    serializer_class = ApplySerializer

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

class SortAPIView(generics.ListAPIView):
    queryset = Apply.objects.all()
    serializer_class = ApplySerializer

    def get_object(self, pk):
        try:
            return Apply.objects.get(pk=pk)
        except Apply.DoesNotExist:
            raise Http404
    
    # Sort의 detail 보기
    def get(self, request, major, format=None):
        major = Major.objects.get(id=major)
        is_ascending_1 = major.priority_1.is_ascending if major.priority_1 else None
        is_ascending_2 = major.priority_2.is_ascending if major.priority_2 else None
        is_ascending_3 = major.priority_3.is_ascending if major.priority_3 else None

        base_rule =  "created_at" if major.is_baserule_FCFS else '?'

        if is_ascending_1 == None :
            sort = Apply.objects.filter(major=major).order_by(
                base_rule
            )
        elif is_ascending_2 == None :
            sort = Apply.objects.filter(major=major).order_by(
                ('priority_1_answer' if is_ascending_1 else '-priority_1_answer'),
                base_rule
            )
        elif is_ascending_3 == None:
            sort = Apply.objects.filter(major=major).order_by(
                ('priority_1_answer' if is_ascending_1 else '-priority_1_answer'),
                ('priority_2_answer' if is_ascending_2 else '-priority_2_answer'),
                base_rule
            )
            sort = sort.annotate(rank=Window(expression=RowNumber(), order_by=(
                F('priority_1_answer').desc(),
                F('priority_2_answer').desc(),
                )))
        else :
            sort = Apply.objects.filter(major=major).order_by(
                ('priority_1_answer' if is_ascending_1 else '-priority_1_answer'),
                ('priority_2_answer' if is_ascending_2 else '-priority_2_answer'),
                ('priority_3_answer' if is_ascending_3 else '-priority_3_answer'),
                base_rule
            )

        serializer = SortSerializer(sort, many=True).data

        for index, data in enumerate(serializer):
            data['rank'] = index + 1

        return Response(serializer)

# sort_apply 명령을 실행
def sort_apply_command_view(request):
    call_command('sort_apply')
    return Response({'message': 'Apply data sorted successfully!'})
from django.forms import ValidationError
from rest_framework import status
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from django.core.management import call_command
from django.db import connections
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer

from apply.models import Apply, Sort
from major.models import Major
from apply.serializers import ApplySerializer, ApplyPostSerializer, SortSerializer, SortPostSerializer


class ApplyAPIView(APIView):
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
        serializer = ApplySerializer(data = request.data) # json을 변환하게 된다.
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
    

class SortAPIView(APIView):
    def get(self, request, **kwargs):
        try:
            if request.GET: # 쿼리 존재시, 쿼리로 필터링한 데이터 전송.
                params = request.GET
                params = {key: (lambda x: params.get(key))(value) for key, value in params.items()}
                sorts = Sort.objects.filter(**params)
            else: # 쿼리 없을 시, 전체 데이터 요청
                sorts = Sort.objects.all()
            serializer = SortSerializer(sorts, many=True)
            return Response(serializer.data)
        except ValidationError as err:
                return Response({'detail': f'{err}'}, status=status.HTTP_400_BAD_REQUEST)

# 특정 학과에 대한 get        
class SortMajorAPIView(APIView):
    def get(self, request, major_name, **kwargs):
        table_name = f"{major_name}_sort"

        with connections['default'].cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name}")
            results = cursor.fetchall()
    
        try:
        #     if request.GET:  # 쿼리 존재시, 쿼리로 필터링한 데이터 전송.
        #         params = request.GET
        #         params = {key: (lambda x: params.get(key))(value) for key, value in params.items()}
        #         sorts = Sort.objects.using(table_name).filter(**params)
        #     else:  # 쿼리 없을 시, 전체 데이터 요청
        #         sorts = Sort.objects.using(table_name).all()

            instances = [Sort(*result) for result in results]
            serializer = SortSerializer(instances, many=True)
        
            try:
                major = Major.objects.get(name=major_name)
                major_id = major.id
                call_command('sort_apply_bymajor', str(major_id))
            except Major.DoesNotExist:
                # Major 객체가 존재하지 않을 경우 예외 처리
                return Response({'detail': f'Major with name {major_name} does not exist'}, status=status.HTTP_404_NOT_FOUND)

            # 정렬 명령 실행
            call_command('sort_apply_bymajor', str(major_id))

            return Response(serializer.data)
        except ValidationError as err:
            return Response({'detail': f'{err}'}, status=status.HTTP_400_BAD_REQUEST)

class SortDetail(APIView):
    def get_object(self, pk):
        try:
            return Sort.objects.get(pk=pk)
        except Apply.DoesNotExist:
            raise Http404
    
    # Sort의 detail 보기
    def get(self, request, pk, format=None):
        sort = self.get_object(pk)
        serializer = SortSerializer(sort)
        return Response(serializer.data)

    # Sort 수정하기는 형평성 우려로 허용되지 않음

    # Sort 삭제하기
    def delete(self, request, pk, format=None):
        apply = self.get_object(pk)
        apply.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# sort_apply 명령을 실행
def sort_apply_command_view(request):
    call_command('sort_apply')
    return Response({'message': 'Apply data sorted successfully!'})

# sort_apply_bymajor 명령을 실행
def sort_apply_bymajor_command_view(request, major_id):
    major = get_object_or_404(Major, id=major_id)  # major_id를 요청 매개변수로 받습니다.

    call_command('sort_apply_bymajor', str(major_id))  # major_id를 문자열로 변환하여 명령을 호출합니다.
    
    # response = Response({'message': 'Apply data sorted successfully!'})
    # response.accepted_renderer = JSONRenderer()

    # return response
from django_seed import Seed
import random
from django.forms import ValidationError
from faker import Faker
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from apply.models import Apply
from locker.models import Building, Locker

from major.models import Major
from major.serializers import MajorSerializer, MajorRequestSerializer
from user.models import User
from django.core.management import call_command


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
        def generate_priority_answer(priority):
                if priority in ["재학여부", "통학여부", "학생회비 납부여부"]:
                    return random.choice([True, False])
                elif priority == "통학시간":
                    return random.randint(1, 150)
                elif priority == "고학번":
                    return random.randint(16, 23)
                elif priority == "전공수업수":
                    return random.randint(1, 7)
                else:
                    return None

        lockers = Locker.objects.filter(major=pk)
        lockers_building = lockers.values_list('building_id', flat=True).distinct()
        print(lockers_building, '빌딩 데이터')

        seeder = Seed.seeder()
        fake = Faker()

        users = User.objects.all()


        major = self.get_object(pk)

        serializer = MajorRequestSerializer(major, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()

            major = self.get_object(pk)
            for user in users :
                seeder.add_entity(Apply, 1, {
                    'major': lambda x: Major.objects.filter(id__in=[pk]).order_by('?').first(), # 테스트 용
                    'user': user,
                    'building_id': lambda x: Building.objects.filter(id__in=lockers_building).order_by('?').first(),
                    'priority_1_answer': lambda x: generate_priority_answer(request.data["priority_1"]),
                    'priority_2_answer': lambda x: generate_priority_answer(request.data["priority_2"]),
                    'priority_3_answer': lambda x: generate_priority_answer(request.data["priority_3"]),
                    'created_at': lambda x: fake.date_time_between(start_date='-3d', end_date='now')
                })

            seeder.execute()
            print("Apply data, Success!")
            # self.stdout.write(self.style.SUCCESS("Apply data, Success!"))

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
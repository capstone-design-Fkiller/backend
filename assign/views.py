from django.forms import ValidationError
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
import json

from user.models import User
from apply.models import Apply
from major.models import Major
from locker.models import Locker
from assign.models import Assign, Unassign
from assign.serializers import AssignSerializer, AssignPostSerializer, UnassignSerializer

class AssignAPIView(APIView):
    queryset = Assign.objects.all()
    serializer_class = AssignSerializer

    def get_object(self, pk):
        try:
            return Assign.objects.get(pk=pk)
        except Assign.DoesNotExist:
            raise Http404
    
    # Assign의 학과별 get
    def get(self, request, major, format=None):
        assign = Assign.objects.filter(major=major)
        serializer = AssignSerializer(assign, many=True).data
        return Response(serializer)
    
    # 학과 사물함을 user에게 assign 
    def post(self, request, major, format=None):
        assigned = []

        # JSON 파싱
        json_data = json.dumps(request.data)
        with open('data.json', 'w') as fp:
            fp.write(json_data)
        data = json.loads(json_data)

        assign_list = data["list"]
        major = Major.objects.get(id=major)

        # 배정할 신청정보 리스트를 순회
        for apply_id in assign_list:
            apply = Apply.objects.get(id=apply_id)
            building_id = apply.building_id
            user = apply.user

            # 아직 배정되지 않은 사물함을 학과, 건물 필터 씌우고 가져옴
            lockers = Locker.objects.filter(major=major, building_id=building_id, owned_id=None)

            for locker in lockers :
                if locker.owned_id is None :  # 사용자 배정 안받은 사물함
                    # Assign 필드 값 지정하고 저장 : 배정
                    assign_instance = Assign.objects.create(
                        user=user,
                        building_id=building_id,
                        locker=locker,
                        apply=apply,
                        major=major
                    )
                    assign_instance.save()
                    assigned.append(assign_instance)

                    # 사물함 정보 수정
                    locker.owned_id = apply.user
                    locker.save()
                    # 사용자 정보 수정
                    user.locker = locker
                    #user.locker = locker
                    user.save()

                    print("| 신청", apply_id,
                          "| 이름", apply.user,
                          "| 건물번호", building_id,
                          "| 사물함번호", locker.locker_number)

                    break
                
            print('남은 사물함의 수', len(lockers))
            if len(lockers) == 0 : # 모든 사물함이 배정됨
                # Unassign 필드 값 지정하고 저장 : 탈락
                unanssign_instance = Unassign.objects.create(user=user, apply=apply, major=major)
                unanssign_instance.save()

                print("debug : 탈락!", "| 신청", apply_id, "| 이름", apply.user)

        serializer = AssignPostSerializer(assigned, many=True)

        return Response(serializer.data)

    # Assign 삭제는 곧 반납을 의미
    def delete(self, request, major, format=None):
        major = Major.objects.get(id=major)

        users = User.objects.filter(major=major)
        lockers = Locker.objects.filter(major=major)

        # locker의 필드값 수정
        for locker in lockers :
            if locker.owned_id is not None :
                locker.owned_id = None
                locker.save()
        # user의 필드값 수정
        for user in users :
            if user.locker is not None :
                user.locker = None
                user.save()

        assigns = Assign.objects.filter(major=major)
        for assign in assigns :
            assign.delete()
            print("assign DB 삭제 완료")
        unassigns = Unassign.objects.filter(major=major)
        for unassign in unassigns:
            unassign.delete()
            print("unassign DB 삭제 완료")

        return Response(status=status.HTTP_204_NO_CONTENT)
    
class UnassignAPIView(APIView):
    queryset = Unassign.objects.all()
    serializer_class = UnassignSerializer

    def get_object(self, pk):
        try:
            return Unassign.objects.get(pk=pk)
        except Unassign.DoesNotExist:
            raise Http404
    
    # Unassign의 학과별 get
    def get(self, request, major, format=None):
        unassign = Unassign.objects.filter(major=major)
        serializer = UnassignSerializer(unassign, many=True).data
        return Response(serializer)
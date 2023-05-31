from django.forms import ValidationError
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from datetime import datetime

from locker.models import Locker
from locker.serializers import LockerSerializer, LockerRequestSerializer

class LockerAPIView(generics.ListCreateAPIView):
    queryset = lockers = Locker.objects.all()
    serializer_class = LockerSerializer

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
        serializer = LockerRequestSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LockerDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LockerSerializer

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
    # 락커 배정 owned_id를 바꿀 때 보내면 된다
    # owned_id가 존재하고  is_shareregistered 값이 들어온 경우, is_shareregistered를 업데이트 한다.
    # 쉐어 신청을 하는 과정에는 is_shareregistered가 true인 사물함들을 보여준다.
    # 쉐어 신청을 완료 할 때는 사용자의 승인 없다고 치고, 사물

    def patch(self, request, pk, format=None):
        shared_id = request.data.get('shared_id')
        
        # 이미 신청한 학생인지 확인
        if shared_id:
            if Locker.objects.filter(shared_id=shared_id).exists():
                return Response({'message': '이미 사물함을 쉐어하고 있는 사용자입니다'}, status=status.HTTP_400_BAD_REQUEST)

        locker = self.get_object(pk)
        serializer = LockerRequestSerializer(locker, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk, format=None):
        shared_id = request.data.get('shared_id')
        
        # 이미 신청한 학생인지 확인
        if shared_id:
            lockers = Locker.objects.filter(shared_id=shared_id)
            if lockers.exists():
                serializer = LockerSerializer(lockers, many=True)
                return Response({'message': f'{shared_id}는 이미 사물함을 쉐어하고 있는 사용자입니다'}, status=status.HTTP_400_BAD_REQUEST)

        locker = self.get_object(pk)
        serializer = LockerRequestSerializer(locker, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # 들어 온 값 저장 후 확인
            locker = self.get_object(pk)

            # 배정되지 않은 사물함일 경우, 쉐어 불가 처리
            if locker.owned_id == None:
                serializer.save(share_start_date = None, share_end_date = None, is_share_registered = False, shared_id = None)
                return Response({'message': f'{locker.id}사물함은 아직 배정되지 않았습니다. 쉐어 불가'}, status=status.HTTP_400_BAD_REQUEST)

            # 날짜 둘 다 존재할 경우,
            if locker.share_start_date and locker.share_end_date:
                # 쉐어중인 사람이 있으면, registered가 False로 된다.
                now = datetime.now()  # 현재 날짜
                if now < locker.share_end_date:
                    print("아직 쉐어 등록 가능")
                    if locker.shared_id:
                        serializer.save(is_share_registered=False)
                    else:
                        serializer.save(is_share_registered=True) # 쉐어중인 사람이 없으면, registered가 True로 된다.
                else :
                    print("쉐어기간이 지났습니다.")
                    serializer.save(is_share_registered=False, share_start_date=None, share_end_date=None, shared_id=None)
                
            #쉐어 날짜가 둘 다 없을 경우, 자동으로 등록이 없으며, 쉐어 중인 사람도 None이 된다.
            elif locker.share_start_date == None and locker.share_end_date == None:
                serializer.save(is_share_registered=False, shared_id=None)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Locker 삭제하기
    def delete(self, request, pk, format=None):
        locker = self.get_object(pk)
        locker.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
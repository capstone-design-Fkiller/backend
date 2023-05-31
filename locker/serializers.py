from major.serializers import MajorSerializer, MajorNameSerializer
from user.serializers import UserSerializer
from user.models import User
from rest_framework import serializers
from major.models import Major
from .models import Building, Locker

class LockerSerializer(serializers.ModelSerializer):
    major = serializers.CharField(source='major.name', read_only=True)  # major 필드에 user.major.name 값을 serialize -> {major = "ELLT"} 로 출력
    floor = serializers.CharField(read_only=True)
    # major = MajorNameSerializer() # {major = {"name": ELLT"}} 로 출력 Major model에서 field를 name만 설정한 것.
    # major = MajorSerializer() # {major = {major의 모든 정보}} 로 출력 => 이 셋 중에 결정하면 되겠다.
    # owned_id = serializers.IntegerField(source='owned_id.id', allow_null=True)
    # owned_id = UserSerializer()
    class Meta:
        model = Locker
        fields = '__all__'

class LockerRequestSerializer(serializers.ModelSerializer):
    # floor= serializers.PrimaryKeyRelatedField(queryset=RelatedModel.objects.all(), required=False)
    floor = serializers.CharField(read_only=True, default="")
    major= serializers.PrimaryKeyRelatedField(queryset=Major.objects.all(), required=False)
    building_id= serializers.PrimaryKeyRelatedField(queryset=Building.objects.all(), required=False)

    
    # def update(self, instance, validated_data):
    #     share_start_date = validated_data.get('share_start_date')
    #     share_end_date = validated_data.get('share_end_date')
    #     is_share_registered = validated_data.get('is_share_registered')
    #     shared_id = validated_data.get('shared_id')

    #     # if (is_share_registered == False):
    #     #     validated_data['share_start_date'] = None
    #     #     validated_data['share_end_date'] = None
    #     #     validated_data['is_share_registered'] = False
    #     #     return super().update(instance, validated_data)
    #     print(instance.shared_id, "인스턴스 ")
    #     print(shared_id, "들어온 거")
    #     if (share_start_date == None) and (share_end_date == None) and (shared_id == None):
    #         validated_data['is_share_registered'] = False
    #         validated_data['shared_id'] = None
    #         return super().update(instance, validated_data)
    #     elif (share_start_date != None) and (share_end_date != None):
    #         if (instance.shared_id != None) and (shared_id == None):
    #             print(instance.shared_id, "인스턴스1 ")
    #             print(shared_id, "들어온 거1")
    #             validated_data['is_share_registered'] = True
    #             return super().update(instance, validated_data)
    #         elif (instance.shared_id != None) or (shared_id != None):
    #             print(instance.shared_id, "인스턴스2 ")
    #             print(shared_id, "들어온 거2")
    #             validated_data['is_share_registered'] = False
    #             return super().update(instance, validated_data)
    #         else:
    #             return super().update(instance, validated_data)
    #     else:
    #         return super().update(instance, validated_data)

    class Meta:
        model = Locker
        fields = '__all__'
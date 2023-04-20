from major.serializers import MajorSerializer, MajorNameSerializer
from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    # major = serializers.CharField(source='major.name')  # major 필드에 user.major.name 값을 serialize -> {major = "ELLT"} 로 출력
    # major = MajorNameSerializer() # {major = {"name": ELLT"}} 로 출력 Major model에서 field를 name만 설정한 것.
    major = MajorSerializer() # {major = {major의 모든 정보}} 로 출력 => 이 셋 중에 결정하면 되겠다.
    class Meta:
        model = User
        fields = '__all__'


class UserMajorSerializer(serializers.ModelSerializer):
    major = serializers.CharField(source='major.name')  # major 필드에 user.major.name 값을 serialize -> {major = "ELLT"} 로 출력
    # major = MajorNameSerializer() # {major = {"name": ELLT"}} 로 출력 Major model에서 field를 name만 설정한 것.
    # major = MajorSerializer() # {major = {major의 모든 정보}} 로 출력 => 이 셋 중에 결정하면 되겠다.
    class Meta:
        model = User
        # fields = ('major',)
        fields = '__all__'

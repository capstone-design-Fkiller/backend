from major.serializers import MajorSerializer, MajorNameSerializer
from .models import Accounts
from rest_framework import serializers
from major.models import Major


class AccountsSerializer(serializers.ModelSerializer):
    # major = serializers.CharField(source='major.name')  # major 필드에 user.major.name 값을 serialize -> {major = "ELLT"} 로 출력
    # major = MajorNameSerializer() # {major = {"name": ELLT"}} 로 출력 Major model에서 field를 name만 설정한 것.
    # major = MajorSerializer() # {major = {major의 모든 정보}} 로 출력 => 이 셋 중에 결정하면 되겠다.
    class Meta:
        model = Accounts
        fields = '__all__'

class AccountsPostSerializer(serializers.ModelSerializer):
    # 포스트할 때는 학과 번호로 저장
    # major = serializers.CharField(source='major.name')  # major 필드에 user.major.name 값을 serialize -> {major = "ELLT"} 로 출력
    # major = MajorNameSerializer() # {major = {"name": ELLT"}} 로 출력 Major model에서 field를 name만 설정한 것.
    # major = MajorSerializer() # {major = {major의 모든 정보}} 로 출력 => 이 셋 중에 결정하면 되겠다.
    class Meta:
        model = Accounts
        fields = '__all__'

# serializers.py

from dj_rest_auth.registration.serializers import RegisterSerializer

class MyUserRegistrationSerializer(RegisterSerializer):
    # username=None
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    major = serializers.PrimaryKeyRelatedField(queryset=Major.objects.all()) #얘가 생기니까 major 필드가 생기더라
    
    # def get_cleaned_data(self):
        # data_dict = super().get_cleaned_data()
        # data_dict['major'] = self.validated_data.get('major')
        # return data_dict

    def custom_signup(self, request, user):
        user.set_password(self.validated_data['password1'])
        major = self.validated_data.get('major') # 이녀석이 요물
        user.major = major 
        # id = self.validated_data.get('id')
        # user.id = id
        # user.id = self.cleaned_data.get('id') # 이거 만드니 major가 없어진다. 
        # user.save(update_fields=['id'])
        user.save()

    class Meta:
        model = Accounts
        fields = ('id', 'password1', 'password2', 'major')

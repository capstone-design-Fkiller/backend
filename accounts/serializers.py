from major.serializers import MajorSerializer, MajorNameSerializer
from .models import Accounts
from rest_framework import serializers
from major.models import Major
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyUserRegistrationSerializer(RegisterSerializer):
    # username=None
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    major = serializers.PrimaryKeyRelatedField(allow_null=True, required=False, queryset=Major.objects.all()) #얘가 생기니까 major 필드가 생기더라

    # username 필드를 Serializer에서 제거
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'] = serializers.CharField(required=True, max_length=50)
        self.fields['name'] = serializers.CharField(allow_blank=True, required=False, max_length=50, default="")
        self.fields.pop('username')
        self.fields.pop('email')

    def validate_id(self, id):
        if Accounts.objects.filter(id=id).exists():
            raise serializers.ValidationError(
                'A user with that id already exists.')
        return id

    def custom_signup(self, request, user):
        user.set_password(self.validated_data['password1'])
        major = self.validated_data.get('major') # 이녀석이 요물
        user.major = major
        id = self.validated_data.get('id')
        user.id = id
        user.name = self.validated_data.get('name')
        user.save()
        # user.save(update_fields=['id'])

    class Meta:
        model = Accounts
        fields = ('id', 'name', 'password1', 'password2', 'major')

    # def validate_username(self, value):
    #     if Accounts.objects.filter(username=value).exists():
    #         raise serializers.ValidationError('Username already exists.')
    #     return value


# drf에서는 cleaned_data 없음 그냥 validated_data만 사용
    # def get_cleaned_data(self):
    #     data_dict = super().get_cleaned_data()
    #     data_dict['id'] = self.validated_data.get('id')
    #     data_dict['password1'] = self.validated_data.get('password1')
    #     data_dict['password2'] = self.validated_data.get('password2')
    #     data_dict['major'] = self.validated_data.get('major')
    #     return data_dict
    
    # adapter도 사용 불가
    # def save(self, request):
    #     adapter = get_adapter()
    #     user = Accounts(
    #         id=self.validated_data.get('id'),
    #         password=self.validated_data.get('password1'),
    #         is_active=False,
    #     )
    #     adapter.save_user(request, user, self)
    #     return user

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


# class LoginSerializer(serializers.Serializer):
#     id = serializers.CharField()
#     password = serializers.CharField()

#     def validate(self, data):
#         user = authenticate(request=self.context.get('request'),
#                             username=data.get('id'),
#                             password=data.get('password'))

#         if not user:
#             raise serializers.ValidationError('Invalid credentials')

#         data['user'] = user
#         return data

class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['id'] = user.id
        token['password'] = user.password

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        return data

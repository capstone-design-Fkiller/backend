from .models import User
from rest_framework import serializers
from major.models import Major
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError as DjangoValidationError
from allauth.account.adapter import get_adapter

# 회원가입 시리얼라이저
class UserRegistrationSerializer(RegisterSerializer):
    id = serializers.CharField(required=True)
    major = serializers.PrimaryKeyRelatedField(allow_null=True, required=False, queryset=Major.objects.all()) #얘가 생기니까 major 필드가 생기더라
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    # password1 = serializers.CharField(write_only=True, style={'input_type': 'password', 'autocomplete': 'new-password'}) #비밀번호 필드 형식으로 바뀌게 됨!
    # password2 = serializers.CharField(write_only=True, style={'input_type': 'password', 'autocomplete': 'new-password'})
    name = serializers.CharField(allow_blank=True, required=False, max_length=50, default="")
    is_usermode = serializers.BooleanField(required=False, default=True)

    # username 필드와 email필드를 Serializer에서 제거
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username') #이렇게 하면 기본으로 있는 필드를 지울 수 있다.
        self.fields.pop('email')

    #나머지 validate는 RegisterSerializer가 알아서 한다.
    def validate_id(self, id):
        if not isinstance(id, str):
            raise serializers.ValidationError("id should be a string")
        if User.objects.filter(id=id).exists():
            raise serializers.ValidationError(
                'A user with that id already exists.')
        return id
    
    def validate_major(self, value):
        # if not value:
            # return None
        if value and not isinstance(value.pk, int) and not isinstance(value.name, str):
            raise serializers.ValidationError("Major value has wrong type value.")
        return value
    
    def validate_is_usermode(self, value):
        if not isinstance(value, bool):
            raise serializers.ValidationError("is_usermode field must be a boolean value")
        return value
    
    def validate_name(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("Name should be a string")
        return value
    
    
    def save(self, request):
        major = self.validated_data.get('major')
        id = self.validated_data.get('id')
        name = self.validated_data.get('name')
        is_usermode = self.validated_data.get('is_usermode') #관리자로 회원가입 추가
        user = User.objects.create_user(id=id, name=name, password=self.validated_data['password1'], major=major, is_usermode=is_usermode)
        return user

    class Meta:
        model = User
        fields = ('id', 'name', 'password1', 'password2', 'is_usermode', 'major')

# 로그인 시리얼라이저
class LoginSerializer(TokenObtainPairSerializer):
    major = serializers.PrimaryKeyRelatedField(allow_null=True, required=False, queryset=Major.objects.all()) #얘가 생기니까 major 필드가 생기더라
    name = serializers.CharField(allow_blank=True, required=False, max_length=50, default="")
    is_usermode = serializers.BooleanField(required=False, default=True)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # token['id'] = user.id
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh_token = self.get_token(self.user)

        user = authenticate(request=self.context.get('request'),
                            id=attrs.get('id'),
                            password=attrs.get('password'))

        if not user:
            raise serializers.ValidationError('Invalid credentials')
        
        if not user.major: # major가 정해져 있지 않으면 정할 수 있게 변경
            user.major = attrs.get('major')

        if not user.name: # name이 정해져 있지 않으면 정할 수 있게 변경
            user.name = attrs.get('name')

        user.is_usermode = attrs.get('is_usermode') #로그인시 is_usermode 값을 보내주면 그에 따라 true로 보내준다.
        user.save(update_fields=['major', 'name', 'is_usermode',])

        data["refresh_token"] = str(refresh_token)
        data["access_token"] = str(refresh_token.access_token)

        return data
    
    def validate_major(self, value):
        # if not value:
            # return None
        if value and not isinstance(value.pk, int) and not isinstance(value.name, str):
            raise serializers.ValidationError("Major value has wrong type value.")
        return value
    
    def validate_is_usermode(self, value):
        if not isinstance(value, bool):
            raise serializers.ValidationError("is_usermode field must be a boolean value")
        return value
    
    def validate_name(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("Name should be a string")
        return value

    class Meta:
        model = User
        fields = ('id', 'name', 'password1', 'password2', 'is_usermode', 'major')

class UserSerializer(serializers.ModelSerializer):
    major = serializers.CharField(source='major.name', allow_null=True)  # major 필드에 user.major.name 값을 serialize -> {major = "ELLT"} 로 출력
    # major = MajorNameSerializer() # {major = {"name": ELLT"}} 로 출력 Major model에서 field를 name만 설정한 것.
    # major = MajorSerializer() # {major = {major의 모든 정보}} 로 출력 => 이 셋 중에 결정하면 되겠다.
    class Meta:
        model = User
        fields = '__all__'

class UserMajorSerializer(serializers.ModelSerializer):
    # major = MajorNameSerializer() # {major = {"name": ELLT"}} 로 출력 Major model에서 field를 name만 설정한 것.
    # major = MajorSerializer() # {major = {major의 모든 정보}} 로 출력 => 이 셋 중에 결정하면 되겠다.
    class Meta:
        model = User
        fields = '__all__'



# # 로그인 시리얼라이저 다른 방식
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


from .models import User
from rest_framework import serializers
from major.models import Major
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

# 회원가입 시리얼라이저
class UserRegistrationSerializer(RegisterSerializer):
    # username=None
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    major = serializers.PrimaryKeyRelatedField(allow_null=True, required=False, queryset=Major.objects.all()) #얘가 생기니까 major 필드가 생기더라

    # username 필드를 Serializer에서 제거
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'] = serializers.CharField(required=True, max_length=50)
        self.fields['name'] = serializers.CharField(allow_blank=True, required=False, max_length=50, default="")
        self.fields['is_admin'] = serializers.BooleanField(required=False, default=False)
        self.fields.pop('username')
        self.fields.pop('email')

    def validate_id(self, id):
        if User.objects.filter(id=id).exists():
            raise serializers.ValidationError(
                'A user with that id already exists.')
        return id
    
    
    def save(self, request):
        # user.set_password(self.validated_data['password1'])
        major = self.validated_data.get('major')
        id = self.validated_data.get('id')
        name = self.validated_data.get('name')
        is_admin = self.validated_data.get('is_admin') #관리자로 회원가입 추가
        user = User.objects.create_user(id=id, name=name, password=self.validated_data['password1'], major=major, is_admin=is_admin)
        # adapter = get_adapter()
        # user = adapter.new_user(request)
        # self.cleaned_data = self.get_cleaned_data()
        # user = adapter.save_user(request, user, self, commit=False)
        # if "password1" in self.cleaned_data:
            # try:
                # adapter.clean_password(self.cleaned_data['password1'], user=user)
            # except DjangoValidationError as exc:
                # raise serializers.ValidationError(
                    # detail=serializers.as_serializer_error(exc)
            # )
        # user.save()
        # self.custom_signup(request, user)
        # setup_user_email(request, user, [])
        return user

    # def custom_signup(self, request, user):
    #     user.set_password(self.validated_data['password1'])
    #     major = self.validated_data.get('major') # 이녀석이 요물
    #     id = self.validated_data.get('id')
    #     name = self.validated_data.get('name')
    #     User.objects.create_user(user=user, id=id, name=name, password=self.validated_data['password1'], major=major)
    #     user.major = major
    #     user.id = id
    #     user.name = self.validated_data.get('name')

    #     user.save()
    #     # user.save(update_fields=['id'])

    class Meta:
        model = User
        fields = ('id', 'name', 'password1', 'password2', 'is_admin', 'major')

# 로그인 시리얼라이저
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

class UserSerializer(serializers.ModelSerializer):
    major = serializers.CharField(source='major.name', allow_null=True)  # major 필드에 user.major.name 값을 serialize -> {major = "ELLT"} 로 출력
    # major = MajorNameSerializer() # {major = {"name": ELLT"}} 로 출력 Major model에서 field를 name만 설정한 것.
    # major = MajorSerializer() # {major = {major의 모든 정보}} 로 출력 => 이 셋 중에 결정하면 되겠다.
    class Meta:
        model = User
        fields = '__all__'

class UserPostSerializer(serializers.ModelSerializer):
    # 포스트할 때는 학과 번호로 저장
    # major = serializers.CharField(source='major.name')  # major 필드에 user.major.name 값을 serialize -> {major = "ELLT"} 로 출력
    # major = MajorNameSerializer() # {major = {"name": ELLT"}} 로 출력 Major model에서 field를 name만 설정한 것.
    # major = MajorSerializer() # {major = {major의 모든 정보}} 로 출력 => 이 셋 중에 결정하면 되겠다.
    class Meta:
        model = User
        fields = '__all__'



# 로그인 시리얼라이저 다른 방식
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


from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.backends import ModelBackend
from dj_rest_auth.views import LoginView
from django.contrib.auth import authenticate, get_user_model
from django.http import Http404

from user.models import User
from user.serializers import UserPostSerializer, UserSerializer

from dj_rest_auth.registration.views import RegisterView
from .serializers import UserRegistrationSerializer
from .serializers import LoginSerializer
from rest_framework import serializers

class MyUserRegistrationView(RegisterView):
    serializer_class = UserRegistrationSerializer

    # # 회원가입 시에 토큰 보내줄 때
    # def post(self, request):
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         user = serializer.save(request)
    #         refresh_token = RefreshToken.for_user(user)

    #         response_data = {
    #             "refresh_token": str(refresh_token),
    #             "access_token": str(refresh_token.access_token),
    #             "user": UserSerializer(user).data
    #         }
    #         return Response(response_data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            id = request.data['id']
            password = request.data['password']
            user = authenticate(request, username=id, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            # user = User.objects.filter(id=id).first() # 둘 중 하나
            user = UserSerializer(user)
            refresh_token = serializer.validated_data.get('refresh_token') # _token을 뒤에 붙일지 고민하자.
            access_token = serializer.validated_data.get('access_token')

            response_data = {
                    'user': user.data,
                    'refresh_token': str(refresh_token),
                    'access_token': str(access_token),
            }
            response = Response(response_data, status=status.HTTP_200_OK)
            
            response.set_cookie("refresh_token", refresh_token, httponly=True)
            response.set_cookie("access_token", access_token, httponly=True)

            return response
        else: # 그 외
            return Response(
                {"message": "로그인에 실패하였습니다"}, status=status.HTTP_400_BAD_REQUEST
            )

class UserAPIView(APIView):
    def get(self, request):
        users = User.objects.all()

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = UserPostSerializer(data = request.data)
        # serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        users = User.objects.all()
        users.delete()
        return Response(request.data, status=status.HTTP_201_CREATED)
    
class UserDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    
    # User의 detail 보기
    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    # User 수정하기
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # User 삭제하기
    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# 로그인뷰 다른 방식
# class LoginView(generics.GenericAPIView):
#     serializer_class = LoginSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         id = serializer.validated_data['id']
#         password = serializer.validated_data['password']

#         user = authenticate(request, id=id, password=password)

#         if not user:
#             return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        

#         refresh = RefreshToken.for_user(user)
#         user = UserSerializer(user) 
#         # response.set_cookie("refresh_token", refresh_token, httponly=True)
#         # response.set_cookie("access_token", access_token, httponly=True)

#         return Response({
#             'user': user.data,
#             'refresh': str(refresh),
#             'access': str(refresh.access_token)
#         })
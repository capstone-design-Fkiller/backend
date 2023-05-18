from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate, get_user_model
from django.http import Http404
import jwt
from user.models import User
from user.serializers import UserSerializer
from backend.settings import SECRET_KEY

from dj_rest_auth.registration.views import RegisterView
from .serializers import RegistrationSerializer
from .serializers import LoginSerializer
from rest_framework import serializers

class RegistrationView(RegisterView):
    serializer_class = RegistrationSerializer


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

        # 유저 정보 확인
    def get(self, request):
        try:
            # access token을 decode 해서 유저 id 추출 => 유저 식별
            access_token = request.COOKIES['access_token']
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('id')
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            data = {'refresh_token': request.COOKIES.get('refresh_token', None)}
            serializer = self.get_serializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access_token = serializer.validated_data.get('access_token', None)
                refresh_token = serializer.validated_data.get('refresh_token', None)
                payload = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('id')
                user = get_object_or_404(User, pk=pk)
                serializer = UserSerializer(instance=user)
                res = Response(serializer.data, status=status.HTTP_200_OK)
                res.set_cookie('access_token', access_token)
                res.set_cookie('refresh_token', refresh_token)
                return res
            raise jwt.exceptions.InvalidTokenError

        except(jwt.exceptions.InvalidTokenError):
            # 사용 불가능한 토큰일 때
            return Response("Token is Invalid",status=status.HTTP_400_BAD_REQUEST)
        except KeyError as err:
                return Response({'message': f'There is no {err}, Please login again'}, status=status.HTTP_400_BAD_REQUEST)

    
    def post(self, request):
        id = request.data['id']
        password = request.data['password']

        user = authenticate(request, id=id, password=password)
        
        if not user:
                raise serializers.ValidationError('the user is not exist or Invalid credentials')
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            refresh_token = serializer.validated_data.get('refresh_token')
            access_token = serializer.validated_data.get('access_token')

            response_data = {
                    'message':  "login success",
                    # 'refresh_token': str(refresh_token),
                    # 'access_token': str(access_token),
            }   
            response = Response(response_data, status=status.HTTP_200_OK)
            
            response.set_cookie("refresh_token", refresh_token, httponly=True)
            response.set_cookie("access_token", access_token, httponly=True)

            return response
        else: # 그 외
            return Response(
                {"message": "로그인에 실패하였습니다"}, status=status.HTTP_400_BAD_REQUEST
            )

class LogoutView(APIView):    
    # 로그아웃
    def get(self, request):
        # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
        response = Response({
            "message": "Logout success"
            }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response

class UserAPIView(APIView):
    def get(self, request, **kwargs):
        try:
            if request.GET: # 쿼리 존재시, 쿼리로 필터링한 데이터 전송.
                params = request.GET
                params = {key: (lambda x: params.get(key))(value) for key, value in params.items()}
                users = User.objects.filter(**params)
            else: # 쿼리 없을 시, 전체 데이터 요청
                users = User.objects.all()

            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        except ValidationError as err:
                return Response({'detail': f'{err}'}, status=status.HTTP_400_BAD_REQUEST)
    
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
    def get(self, request, pk, format=None, **kwargs):
        # filteredUser = User.objects.filter(**kwargs)

        user = self.get_object(pk)
        serializer = UserSerializer(user)
        # serializer = UserSerializer(filteredUser)
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
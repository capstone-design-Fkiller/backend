import json
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework.authentication import TokenAuthentication
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

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RegistrationView(RegisterView):
    serializer_class = RegistrationSerializer

    @swagger_auto_schema(
        tags=["회원가입"], request_body=RegistrationSerializer, responses={200: "Success"}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    authentication_classes = [TokenAuthentication]

    # 유저 정보 확인
    @swagger_auto_schema(
        tags=["로그인 : 유저 정보를 가져옵니다."],
        operation_description="토큰 확인 후 유저 정보를 리턴합니다.",
        manual_parameters=[],
        responses={200: "Success"},
    )
    def get(self, request):
        try:
            auth_header = request.headers["Authorization"]
            access_token = (
                auth_header.split(" ")[1] if len(auth_header.split(" ")) > 1 else None
            )
            print(access_token)
            if access_token != "null":
                access_token = json.loads(access_token)
                payload = jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])
                pk = payload.get("user_id")
                user = get_object_or_404(User, pk=pk)
                serializer = UserSerializer(instance=user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": f"로그인 해주세요!"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        except jwt.exceptions.ExpiredSignatureError:
            # 엑세스 토큰 만료 시 토큰 갱신, 리프레쉬 토큰 만료 시 Token Error 전송
            refresh_token = request.COOKIES.get("refresh_token", None)
            data = {"refresh": refresh_token}
            serializer = TokenRefreshSerializer(data=data)

            if serializer.is_valid(raise_exception=True):
                access_token = serializer.validated_data.get("access", None)
                print("여기니~~2")
                payload = jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])
                pk = payload.get("user_id")
                user = get_object_or_404(User, pk=pk)
                serializer = UserSerializer(instance=user)
                response = Response(serializer.data, status=status.HTTP_200_OK)
                response.set_cookie("access_token", access_token)
                response.set_cookie("refresh_token", refresh_token)
                return response
        except KeyError as err:
            return Response(
                {"message": f"There is no {err}, Please login again"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    @swagger_auto_schema(
        tags=["로그인"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER, default=201801910),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, default="qwer1234!"
                ),
            },
            required=["id", "password"],
        ),
        responses={200: "Success"},
    )
    def post(self, request):
        try:
            id = request.data["id"]
            password = request.data["password"]

            user = authenticate(request, id=id, password=password)

            if not user:
                raise serializers.ValidationError("존재하지 않는 유저입니다.")
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                refresh_token = serializer.validated_data.get("refresh_token")
                access_token = serializer.validated_data.get("access_token")

                response_data = {
                    "message": "login success",
                    "refresh_token": str(refresh_token),
                    "access_token": str(access_token),
                }
                response = Response(response_data, status=status.HTTP_200_OK)

                # response.set_cookie("refresh_token", refresh_token, httponly=True)
                response.set_cookie(
                    "Authorization", "Bearer " + str(access_token), httponly=True
                )
                response.set_cookie("access_token", access_token, httponly=True)

                return response
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    # 로그아웃
    @swagger_auto_schema(
        tags=["로그아웃"],
        operation_description="쿠키에서 토큰을 삭제합니다.",
        manual_parameters=[],
        responses={200: "Success"},
    )
    def get(self, request):
        # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
        try:
            response = Response(
                {"message": "logout success"}, status=status.HTTP_202_ACCEPTED
            )
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")
            return response
        except ValidationError as err:
            return Response(
                {"message": f"{err}, 로그아웃 실패"}, status=status.HTTP_400_BAD_REQUEST
            )


class UserAPIView(APIView):
    id = openapi.Parameter(
        "id",
        openapi.IN_QUERY,
        description="유저 id",
        required=False,
        default=201801910,
        type=openapi.TYPE_INTEGER,
    )
    major = openapi.Parameter(
        "major",
        openapi.IN_QUERY,
        description="major query",
        required=False,
        default=17,
        type=openapi.TYPE_INTEGER,
    )

    @swagger_auto_schema(
        tags=["유저 : 쿼리 유저 정보를 가져옵니다."],
        manual_parameters=[id, major],
        responses={200: "Success"},
    )
    def get(self, request, **kwargs):
        try:
            if request.GET:  # 쿼리 존재시, 쿼리로 필터링한 데이터 전송.
                params = request.GET
                params = {
                    key: (lambda x: params.get(key))(value)
                    for key, value in params.items()
                }
                users = User.objects.filter(**params)
            else:  # 쿼리 없을 시, 전체 데이터 요청
                users = User.objects.all()

            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        except ValidationError as err:
            return Response(
                {"message": f"{err} 유저 정보를 가져오지 못했습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

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
    getUserDetail = openapi.Parameter(
        "id",
        openapi.IN_PATH,
        description="유저 id",
        required=True,
        default=201801910,
        type=openapi.TYPE_INTEGER,
    )

    @swagger_auto_schema(
        tags=["유저 : 개별 유저 정보를 가져옵니다."],
        manual_parameters=[getUserDetail],
        responses={200: "Success"},
    )
    def get(self, request, pk, format=None, **kwargs):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    # User 수정하기
    putUserDetail = openapi.Parameter(
        "id",
        openapi.IN_PATH,
        description="유저 id",
        required=True,
        default=201801910,
        type=openapi.TYPE_INTEGER,
    )

    @swagger_auto_schema(
        tags=["유저 : 개별 유저 정보를 수정합니다."],
        manual_parameters=[putUserDetail],
        responses={200: "Success"},
    )
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

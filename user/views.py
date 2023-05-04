from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.backends import ModelBackend
from dj_rest_auth.views import LoginView
from django.contrib.auth import authenticate, get_user_model
from django.http import Http404

from user.models import User
from user.serializers import UserPostSerializer, UserSerializer

from dj_rest_auth.registration.views import RegisterView
from .serializers import UserRegistrationSerializer
from .serializers import LoginSerializer

class MyUserRegistrationView(RegisterView):
    serializer_class = UserRegistrationSerializer


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


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



# # 로그인뷰 다른 방식
# class LoginView(generics.GenericAPIView):
#     serializer_class = LoginSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user_id = serializer.validated_data['id']
#         password = serializer.validated_data['password']

#         user = authenticate(request, username=user_id, password=password)

#         if not user:
#             return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

#         refresh = RefreshToken.for_user(user)

#         return Response({
#             'user': {
#                 'id': user.id
#             },
#             'refresh': str(refresh),
#             'access': str(refresh.access_token)
#         })
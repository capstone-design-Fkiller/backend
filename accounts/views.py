from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.backends import ModelBackend
from dj_rest_auth.views import LoginView
from django.contrib.auth import authenticate, get_user_model
from django.http import Http404

from accounts.models import Accounts
from accounts.serializers import AccountsPostSerializer, AccountsSerializer

from dj_rest_auth.registration.views import RegisterView
from .serializers import MyUserRegistrationSerializer
from .serializers import LoginSerializer

class MyUserRegistrationView(RegisterView):
    serializer_class = MyUserRegistrationSerializer


# 갈 예정
class AccountsAPIView(APIView):
    def get(self, request):
        accounts = Accounts.objects.all()

        serializer = AccountsSerializer(accounts, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = AccountsPostSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccountsDetail(APIView):
    def get_object(self, pk):
        try:
            return Accounts.objects.get(pk=pk)
        except Accounts.DoesNotExist:
            raise Http404
    
    # Account의 detail 보기
    def get(self, request, pk, format=None):
        account = self.get_object(pk)
        serializer = AccountsSerializer(account)
        return Response(serializer.data)

    # Account 수정하기
    def put(self, request, pk, format=None):
        account = self.get_object(pk)
        serializer = AccountsSerializer(account, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Account 삭제하기
    def delete(self, request, pk, format=None):
        account = self.get_object(pk)
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
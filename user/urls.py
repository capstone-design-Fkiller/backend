from django.urls import path
from user import views
from .views import LoginView, LogoutView

urlpatterns = [
    path('user/', views.UserAPIView.as_view()),
    path('user/<int:pk>', views.UserDetail.as_view()),
    path('registration/', views.RegistrationView.as_view(), name='myuser_register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
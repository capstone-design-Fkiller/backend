from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from accounts import views
from .views import LoginView

urlpatterns = [
    path('accounts/', views.AccountsAPIView.as_view()),
    path('accounts/<int:pk>', views.AccountsDetail.as_view()),
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('auth/registration/', views.MyUserRegistrationView.as_view(), name='myuser_register'),
    path('auth/login/', LoginView.as_view(), name='login')
]

urlpatterns = format_suffix_patterns(urlpatterns)
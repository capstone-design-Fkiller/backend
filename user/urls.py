from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from user import views
from .views import LoginView

urlpatterns = [
    path('user/', views.UserAPIView.as_view()),
    path('user/<int:pk>', views.UserDetail.as_view()),
    path('registration/', views.MyUserRegistrationView.as_view(), name='myuser_register'),
    # path('registration/', include('dj_rest_auth.registration.urls')),
    path('login/', LoginView.as_view(), name='login'),
    path('', include('dj_rest_auth.urls'))
]

urlpatterns = format_suffix_patterns(urlpatterns)
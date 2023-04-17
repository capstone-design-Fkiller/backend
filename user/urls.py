from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from user import views1

urlpatterns = [
    path('user/', views1.UserAPIView.as_view()),
    path('user/<int:pk>', views1.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
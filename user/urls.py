from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from user import views

urlpatterns = [
    path('user/', views.UserAPIView.as_view()),
    path('user/<int:pk>', views.UserDetail.as_view()),
    path('user/major/', views.UserMajor.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
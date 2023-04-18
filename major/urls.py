from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from major import views

urlpatterns = [
    path('major/', views.MajorAPIView.as_view()),
    path('major/<int:pk>', views.MajorDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
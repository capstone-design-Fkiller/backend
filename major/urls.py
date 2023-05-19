from django.urls import path
from major import views

urlpatterns = [
    path('major/', views.MajorAPIView.as_view()),
    path('major/<int:pk>', views.MajorDetail.as_view()),
]
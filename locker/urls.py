from django.urls import path
from locker import views

urlpatterns = [
    path('locker/', views.LockerAPIView.as_view()),
    path('locker/<int:pk>', views.LockerDetail.as_view()),
]
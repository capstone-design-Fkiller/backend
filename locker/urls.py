from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from locker import views

urlpatterns = [
    path('locker/', views.LockerAPIView.as_view()),
    path('locker/<int:pk>', views.LockerDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
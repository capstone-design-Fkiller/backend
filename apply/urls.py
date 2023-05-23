from django.urls import path
from apply import views

urlpatterns = [
    path('apply/', views.ApplyAPIView.as_view()),
    path('apply/<int:pk>', views.ApplyDetail.as_view()),
    path('sort/<int:major>', views.SortAPIView.as_view()),
]

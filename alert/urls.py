from django.urls import path
from alert import views

urlpatterns = [
    path('alert/', views.AlertView.as_view()),
    path('alert/<int:pk>', views.AlertDetail.as_view()),
]
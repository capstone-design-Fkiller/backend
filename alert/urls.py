from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from alert import views

urlpatterns = [
    path('alert/', views.AlertView.as_view()),
    path('alert/<int:pk>', views.AlertDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from apply import views
from apply.views import sort_apply_command_view

urlpatterns = [
    path('apply/', views.ApplyAPIView.as_view()),
    path('apply/<int:pk>', views.ApplyDetail.as_view()),
    path('sort/<int:major>', views.SortAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
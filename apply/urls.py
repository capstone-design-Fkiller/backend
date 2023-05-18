from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from apply import views
from apply.views import sort_apply_command_view, sort_apply_bymajor_command_view

urlpatterns = [
    path('apply/', views.ApplyAPIView.as_view()),
    path('apply/<int:pk>', views.ApplyDetail.as_view()),
    path('sort/', views.SortAPIView.as_view()),
    path('sort/<int:pk>', views.SortDetail.as_view()),
    path('sort_apply/', sort_apply_command_view, name='sort_apply'),
    path('sort/<str:major_name>/', views.SortMajorAPIView.as_view(), name='sort-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
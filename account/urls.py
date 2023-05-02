from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from account import views

urlpatterns = [
    path('account/', views.AccountAPIView.as_view()),
    path('account/<int:pk>', views.AccountDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
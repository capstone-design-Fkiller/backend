from django.urls import path
from notice import views

urlpatterns = [
    path('notice/', views.NoticeView.as_view()),
    path('notice/<int:pk>', views.NoticeDetail.as_view()),
]
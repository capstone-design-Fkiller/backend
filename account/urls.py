from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from account import views

urlpatterns = [
    path('account/', views.AccountAPIView.as_view()),
    path('account/<int:pk>', views.AccountDetail.as_view()),
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
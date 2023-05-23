from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from assign import views

urlpatterns = [
    path('assign/<int:major>', views.AssignAPIView.as_view()),
    path('unassign/<int:major>', views.UnassignAPIView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
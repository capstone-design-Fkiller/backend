from rest_framework import serializers
from .models import User
from major.models import Major


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
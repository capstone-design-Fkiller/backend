from major.serializers import NameMajorSerializer
from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserMajorSerializer(serializers.ModelSerializer):

    major = NameMajorSerializer()
    class Meta:
        model = User
        # fields = ('major',)
        fields = '__all__'

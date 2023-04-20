from .models import Major
from rest_framework import serializers

class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = '__all__'


class MajorNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = ('name',)
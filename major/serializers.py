from .models import Major
from .models import Priority
from rest_framework import serializers

class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = '__all__'

class MajorSerializer(serializers.ModelSerializer):
    priority_1 = PrioritySerializer()
    priority_2 = PrioritySerializer()
    priority_3 = PrioritySerializer()

    class Meta:
        model = Major
        fields = '__all__'

class MajorNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = ('name',)

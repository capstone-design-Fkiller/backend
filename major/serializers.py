from .models import Major, Priority
from rest_framework import serializers

class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = '__all__'

class MajorSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(read_only=True)  # major 필드에 user.major.name 값을 serialize -> {major = "ELLT"} 로 출력
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

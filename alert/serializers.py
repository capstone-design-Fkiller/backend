from major.models import Major
from .models import Alert
from rest_framework import serializers

class AlertSerializer(serializers.ModelSerializer):
    message = serializers.CharField(max_length=200)
    major = serializers.CharField(source='major.name', allow_null=True)  # major 필드에 user.major.name 값을 serialize -> {major = "ELLT"} 로 출력
    # major = serializers.PrimaryKeyRelatedField(queryset=Major.objects.all())

    
    class Meta:
        model = Alert
        fields = '__all__'


class AlertPostSerializer(serializers.ModelSerializer):
    message = serializers.CharField(max_length=200)
    major = serializers.PrimaryKeyRelatedField(queryset=Major.objects.all())

    # major = serializers.IntegerField(read_only=True)  # major 필드에 user.major.name 값을 serialize -> {major = "ELLT"} 로 출력

    class Meta:
        model = Alert
        fields = '__all__'
        


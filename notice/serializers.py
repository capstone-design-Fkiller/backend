from .models import Notice
from rest_framework import serializers


class NoticeSerializer(serializers.ModelSerializer):
    # major = serializers.CharField(source='major.name', allow_null=True)  # major 필드에 user.major.name 값을 serialize -> {major = "ELLT"} 로 출력

    class Meta:
        model = Notice
        fields = '__all__'
        

class NoticePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notice
        fields = '__all__'
        


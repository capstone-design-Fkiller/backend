from .models import Notice
from rest_framework import serializers


class NoticeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Notice
        fields = '__all__'
        

class NoticePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notice
        fields = '__all__'
        


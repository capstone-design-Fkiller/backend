from .models import Alert
from rest_framework import serializers

class AlertSerializer(serializers.ModelSerializer):
    message = serializers.CharField(max_length=200)
    
    class Meta:
        model = Alert
        fields = '__all__'
        
class AlertPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Alert
        fields = '__all__'
        


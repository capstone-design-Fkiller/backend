from .models import Alert
from rest_framework import serializers


class AlertSerializer(serializers.ModelSerializer):
    # priority_1 = PrioritySerializer() # question answer를 담을 수 있도록
    
    class Meta:
        model = Alert
        fields = '__all__'
        

class AlertPostSerializer(serializers.ModelSerializer):
    # priority_1 = PrioritySerializer() # question answer를 담을 수 있도록

    class Meta:
        model = Alert
        fields = '__all__'
        


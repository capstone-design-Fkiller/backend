from .models import Apply, Priority1
from rest_framework import serializers


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority1
        # fields = '__all__'
        fields = ('question', 'answer')
        

class ApplySerializer(serializers.ModelSerializer):
    priority_1 = PrioritySerializer() # question answer를 담을 수 있도록
    class Meta:
        model = Apply
        fields = '__all__'
        


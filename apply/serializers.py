from major.models import Major
from .models import Apply, Priority1
from rest_framework import serializers


class PrioritySerializer(serializers.ModelSerializer):
    # field_type = serializers.ChoiceField(choices=[('char', 'CharField'), ('int', 'IntegerField'), ('bool', 'BooleanField')])
    # print('test1')
    question = serializers.CharField(source='question.priority_first')  # major 필드에 user.major.name 값을 serialize -> {major = "ELLT"} 로 출력
    answer = serializers.CharField(source='answer.priority_1_answer')  # major 필드에 user.major.name 값을 serialize -> {major = "ELLT"} 로 출력


    class Meta:
        model = Priority1
        fields = '__all__'

class ApplySerializer(serializers.ModelSerializer):
    # priority_1 = PrioritySerializer() # question answer를 담을 수 있도록
    
    class Meta:
        model = Apply
        fields = '__all__'
        

class ApplyPostSerializer(serializers.ModelSerializer):
    # priority_1 = PrioritySerializer() # question answer를 담을 수 있도록

    class Meta:
        model = Apply
        fields = '__all__'
        


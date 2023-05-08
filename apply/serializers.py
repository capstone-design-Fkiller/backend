from .models import Apply, Priority1
from rest_framework import serializers


class PrioritySerializer(serializers.ModelSerializer):
    field_type = serializers.ChoiceField(choices=[('char', 'CharField'), ('int', 'IntegerField'), ('bool', 'BooleanField')])
    print('test1')

    class Meta:
        model = Priority1
        fields = ['question', 'answer', 'field_type']
    
    # 왜 여기로 진입하지를 못할까...?
    def to_internal_value(self, data):
        print('test2')
        field_type = data.get('field_type')
        answer = data.get('answer')
        if field_type == 'int':
            try:
                answer = int(answer)
            except (ValueError, TypeError):
                raise serializers.ValidationError('Invalid value for IntegerField')
        elif field_type == 'bool':
            if answer.lower() in ['true', '1']:
                answer = True
            elif answer.lower() in ['false', '0']:
                answer = False
            else:
                raise serializers.ValidationError('Invalid value for BooleanField')
        print(answer)
        return {'answer': answer}



class ApplySerializer(serializers.ModelSerializer):
    priority_1 = PrioritySerializer() # question answer를 담을 수 있도록
    
    class Meta:
        model = Apply
        fields = '__all__'
        


from .models import Assign, Unassign
from rest_framework import serializers


class AssignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assign
        fields = '__all__'

class AssignPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assign
        fields = '__all__'

class UnassignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Unassign
        fields = '__all__'
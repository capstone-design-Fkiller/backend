from .models import Assign, Unassign
from rest_framework import serializers


class AssignSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Assign
        fields = '__all__'

    def get_user_name(self, obj):
        return obj.user.name

class AssignPostSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Assign
        fields = '__all__'

    def get_user_name(self, obj):
        return obj.user.name

class UnassignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Unassign
        fields = '__all__'
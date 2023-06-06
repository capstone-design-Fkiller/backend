from rest_framework import serializers
from major.models import Major
from .models import Building, Locker

class LockerSerializer(serializers.ModelSerializer):
    major = serializers.CharField(source='major.name', read_only=True)
    floor = serializers.CharField(read_only=True)
    start_date = serializers.DateTimeField(source='major.start_date', read_only=True)
    end_date = serializers.DateTimeField(source='major.end_date', read_only=True)
    owned_name = serializers.SerializerMethodField()
    shared_name = serializers.SerializerMethodField()
    # owned_id = serializers.IntegerField(source='owned_id.id', allow_null=True)
    # owned_id = UserSerializer()
    class Meta:
        model = Locker
        fields = '__all__'

    def get_owned_name(self, obj):
        if obj.owned_id and obj.owned_id.name:
            return obj.owned_id.name
        else:
            return None
    
    def get_shared_name(self, obj):
        if obj.shared_id and obj.shared_id.name:
            return obj.shared_id.name
        else:
            return None

class LockerRequestSerializer(serializers.ModelSerializer):
    # floor= serializers.PrimaryKeyRelatedField(queryset=RelatedModel.objects.all(), required=False)
    floor = serializers.CharField(read_only=True, default="")
    major= serializers.PrimaryKeyRelatedField(queryset=Major.objects.all(), required=False)
    building_id= serializers.PrimaryKeyRelatedField(queryset=Building.objects.all(), required=False)
    
    class Meta:
        model = Locker
        fields = '__all__'
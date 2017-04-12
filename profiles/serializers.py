from rest_framework import serializers

from . import models


class TechSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Technology
        fields = ('id', 'name')


class TechnologyMasteringLevelSerializer(serializers.ModelSerializer):
    technology_name = serializers.CharField(source='technology.name')
    activity_name = serializers.CharField(source='get_activity_display')

    class Meta:
        model = models.TechnologyMasteringLevel
        exclude = ('user', 'removed')


class SearchUserAutoSerializer(serializers.Serializer):
    value = serializers.CharField(source='username')
    data = serializers.CharField(source='url')

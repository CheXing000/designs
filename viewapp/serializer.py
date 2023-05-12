from rest_framework import serializers
from .models import *


class ScenerySerializer(serializers.Serializer):
    city = serializers.CharField(max_length=45)


class ScenerysSerializer(serializers.Serializer):
    scenery = serializers.CharField(max_length=85)
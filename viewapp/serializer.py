from rest_framework import serializers
from .models import *


class ScenerySerializer(serializers.Serializer):
    city = serializers.CharField(max_length=45)


class ScenerysSerializer(serializers.Serializer):
    scenery = serializers.CharField(max_length=85)


class WaysSerialezer(serializers.Serializer):
    scenerys = serializers.CharField(max_length=85)
    start_time = serializers.CharField(max_length=85)
    days = serializers.CharField(max_length=45)
    say_people = serializers.IntegerField()
    is_on = serializers.CharField(max_length=45)



class UserwaySerialezer(serializers.Serializer):
    scenerys = serializers.CharField(max_length=85)
    user = serializers.CharField(max_length=85)
    start_time = serializers.CharField(max_length=85)
    end_time = serializers.CharField(max_length=85)
    days = serializers.CharField(max_length=45)
    say_people = serializers.IntegerField()
    is_on = serializers.CharField(max_length=45)


from datetime import __all__
from rest_framework import serializers
from .models import UserProfile
from .models import Tasks
from django.contrib.auth.models import User
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'email', 'password', 'inspirations']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        def create(self, validated_data):
          return User.objects.create_user(**validated_data)
class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['id', 'title', 'duration', 'description', 'pdf', 'video_link', 'iscomplete', 'inprogress', 'isDone']
        extra_kwargs = {
            # 'inprogress': {'required': False},
            # 'isdone': {'required': False},
            # 'iscomplete': {'required': False},
            'pdf': {'required': False},
            'video_link': {'required': False}
        }    
class LeaderboardEntrySerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    username = serializers.CharField()
    points = serializers.IntegerField()     
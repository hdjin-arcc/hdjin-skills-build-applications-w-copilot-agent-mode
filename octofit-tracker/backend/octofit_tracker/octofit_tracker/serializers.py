from rest_framework import serializers
from .models import User, Team, Activity, Workout, Leaderboard

class UserSerializer(serializers.ModelSerializer):
    """사용자 시리얼라이저"""
    team_count = serializers.SerializerMethodField()
    activity_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'created_at', 'team_count', 'activity_count']
        read_only_fields = ['id', 'created_at']
    
    def get_team_count(self, obj):
        """팀 수"""
        return obj.teams.count()
    
    def get_activity_count(self, obj):
        """활동 수"""
        return obj.activities.count()

class TeamSerializer(serializers.ModelSerializer):
    """팀 시리얼라이저"""
    members = UserSerializer(many=True, read_only=True)
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'members', 'created_at', 'member_count']
        read_only_fields = ['id', 'created_at']
    
    def get_member_count(self, obj):
        """멤버 수"""
        return obj.members.count()

class ActivitySerializer(serializers.ModelSerializer):
    """활동 시리얼라이저"""
    user_name = serializers.CharField(source='user.name', read_only=True)
    
    class Meta:
        model = Activity
        fields = ['id', 'user', 'user_name', 'activity_type', 'duration', 'calories_burned', 'date']
        read_only_fields = ['id', 'date']

class WorkoutSerializer(serializers.ModelSerializer):
    """운동 프로그램 시리얼라이저"""
    exercise_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'exercises', 'difficulty_level', 'created_at', 'exercise_count']
        read_only_fields = ['id', 'created_at']
    
    def get_exercise_count(self, obj):
        """운동 개수"""
        if isinstance(obj.exercises, list):
            return len(obj.exercises)
        return 0

class LeaderboardSerializer(serializers.ModelSerializer):
    """리더보드 시리얼라이저"""
    user = UserSerializer(read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True, allow_null=True)
    
    class Meta:
        model = Leaderboard
        fields = ['id', 'user', 'team', 'team_name', 'total_score', 'rank', 'updated_at']
        read_only_fields = ['id', 'updated_at']

from django.contrib import admin
from .models import User, Team, Activity, Workout, Leaderboard

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """사용자 관리자"""
    list_display = ['name', 'email', 'created_at', 'get_team_count']
    list_filter = ['created_at']
    search_fields = ['name', 'email']
    readonly_fields = ['created_at']
    
    def get_team_count(self, obj):
        return obj.teams.count()
    get_team_count.short_description = '팀 수'

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """팀 관리자"""
    list_display = ['name', 'created_at', 'get_member_count']
    list_filter = ['created_at']
    search_fields = ['name']
    readonly_fields = ['created_at']
    filter_horizontal = ['members']
    
    def get_member_count(self, obj):
        return obj.members.count()
    get_member_count.short_description = '멤버 수'

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """활동 관리자"""
    list_display = ['user', 'activity_type', 'duration', 'calories_burned', 'date']
    list_filter = ['activity_type', 'date', 'user']
    search_fields = ['user__name', 'activity_type']
    readonly_fields = ['date']
    date_hierarchy = 'date'

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    """운동 프로그램 관리자"""
    list_display = ['name', 'difficulty_level', 'created_at', 'get_exercise_count']
    list_filter = ['difficulty_level', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
    
    def get_exercise_count(self, obj):
        if isinstance(obj.exercises, list):
            return len(obj.exercises)
        return 0
    get_exercise_count.short_description = '운동 개수'

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """리더보드 관리자"""
    list_display = ['rank', 'user', 'total_score', 'team', 'updated_at']
    list_filter = ['rank', 'updated_at', 'team']
    search_fields = ['user__name', 'team__name']
    readonly_fields = ['updated_at']
    ordering = ['rank']

from django.db import models
from django.core.validators import MinValueValidator, EmailValidator
from django.core.exceptions import ValidationError

# User Model
class User(models.Model):
    """피트니스 앱 사용자 모델"""
    name = models.CharField(max_length=100, help_text='사용자 이름')
    email = models.EmailField(unique=True, validators=[EmailValidator()], help_text='이메일 주소')
    password = models.CharField(max_length=100, help_text='사용자 비밀번호')
    created_at = models.DateTimeField(auto_now_add=True, help_text='생성 날짜')
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.email})"

# Team Model
class Team(models.Model):
    """팀 모델"""
    name = models.CharField(max_length=100, help_text='팀 이름')
    description = models.TextField(help_text='팀 설명')
    members = models.ManyToManyField(User, related_name='teams', help_text='팀 멤버')
    created_at = models.DateTimeField(auto_now_add=True, help_text='생성 날짜')
    
    class Meta:
        db_table = 'teams'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return self.name

# Activity Model
class Activity(models.Model):
    """활동 기록 모델"""
    ACTIVITY_TYPES = [
        ('Running', '달리기'),
        ('Swimming', '수영'),
        ('Cycling', '자전거'),
        ('Gym', '헬스장'),
        ('Yoga', '요가'),
        ('Walking', '산책'),
        ('Sports', '스포츠'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES, help_text='활동 종류')
    duration = models.IntegerField(validators=[MinValueValidator(1)], help_text='지속시간 (분)')
    calories_burned = models.IntegerField(validators=[MinValueValidator(0)], help_text='소모 칼로리')
    date = models.DateTimeField(auto_now_add=True, help_text='활동 날짜')
    
    class Meta:
        db_table = 'activities'
        ordering = ['-date']
        indexes = [
            models.Index(fields=['user', '-date']),
            models.Index(fields=['activity_type']),
        ]
    
    def __str__(self):
        return f"{self.user.name} - {self.activity_type} ({self.date.strftime('%Y-%m-%d')})"

# Workout Model
class Workout(models.Model):
    """운동 프로그램 모델"""
    DIFFICULTY_LEVELS = [
        ('Easy', '쉬움'),
        ('Medium', '중간'),
        ('Hard', '어려움'),
    ]
    
    name = models.CharField(max_length=100, help_text='운동 프로그램 이름')
    description = models.TextField(help_text='운동 프로그램 설명')
    exercises = models.JSONField(help_text='운동 목록 (JSON 형식)')
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, help_text='난이도')
    created_at = models.DateTimeField(auto_now_add=True, help_text='생성 날짜')
    
    class Meta:
        db_table = 'workouts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['difficulty_level']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.difficulty_level})"

# Leaderboard Model
class Leaderboard(models.Model):
    """리더보드 모델"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='leaderboard')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='leaderboard_entries')
    total_score = models.IntegerField(default=0, validators=[MinValueValidator(0)], help_text='총 점수')
    rank = models.IntegerField(validators=[MinValueValidator(1)], help_text='순위')
    updated_at = models.DateTimeField(auto_now=True, help_text='업데이트 날짜')
    
    class Meta:
        db_table = 'leaderboard'
        ordering = ['rank']
        indexes = [
            models.Index(fields=['rank']),
            models.Index(fields=['total_score']),
        ]
    
    def __str__(self):
        return f"#{self.rank} {self.user.name} ({self.total_score} pts)"

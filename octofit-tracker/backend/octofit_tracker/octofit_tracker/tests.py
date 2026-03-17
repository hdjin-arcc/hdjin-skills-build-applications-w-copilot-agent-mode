from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import User, Team, Activity, Workout, Leaderboard
from datetime import datetime


class UserModelTest(TestCase):
    """사용자 모델 테스트"""
    
    def setUp(self):
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            password='password123'
        )
    
    def test_create_user(self):
        """사용자 생성 테스트"""
        self.assertEqual(self.user.name, 'Test User')
        self.assertEqual(self.user.email, 'test@example.com')
    
    def test_user_str(self):
        """사용자 문자열 표현 테스트"""
        expected_str = f"{self.user.name} ({self.user.email})"
        self.assertEqual(str(self.user), expected_str)
    
    def test_user_email_unique(self):
        """사용자 이메일 고유성 테스트"""
        with self.assertRaises(Exception):
            User.objects.create(
                name='Another User',
                email='test@example.com',
                password='password123'
            )


class TeamModelTest(TestCase):
    """팀 모델 테스트"""
    
    def setUp(self):
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            password='password123'
        )
        self.team = Team.objects.create(
            name='Test Team',
            description='Test Team Description'
        )
        self.team.members.add(self.user)
    
    def test_create_team(self):
        """팀 생성 테스트"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.members.count(), 1)
    
    def test_team_str(self):
        """팀 문자열 표현 테스트"""
        self.assertEqual(str(self.team), self.team.name)


class ActivityModelTest(TestCase):
    """활동 모델 테스트"""
    
    def setUp(self):
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            password='password123'
        )
        self.activity = Activity.objects.create(
            user=self.user,
            activity_type='Running',
            duration=30,
            calories_burned=300
        )
    
    def test_create_activity(self):
        """활동 생성 테스트"""
        self.assertEqual(self.activity.activity_type, 'Running')
        self.assertEqual(self.activity.duration, 30)
        self.assertEqual(self.activity.calories_burned, 300)
    
    def test_activity_str(self):
        """활동 문자열 표현 테스트"""
        self.assertIn(self.user.name, str(self.activity))
        self.assertIn('Running', str(self.activity))


class WorkoutModelTest(TestCase):
    """운동 프로그램 모델 테스트"""
    
    def setUp(self):
        self.workout = Workout.objects.create(
            name='Test Workout',
            description='Test Workout Description',
            exercises=['Exercise 1', 'Exercise 2'],
            difficulty_level='Medium'
        )
    
    def test_create_workout(self):
        """운동 생성 테스트"""
        self.assertEqual(self.workout.name, 'Test Workout')
        self.assertEqual(self.workout.difficulty_level, 'Medium')
        self.assertEqual(len(self.workout.exercises), 2)
    
    def test_workout_str(self):
        """운동 문자열 표현 테스트"""
        expected_str = f"{self.workout.name} ({self.workout.difficulty_level})"
        self.assertEqual(str(self.workout), expected_str)


class LeaderboardModelTest(TestCase):
    """리더보드 모델 테스트"""
    
    def setUp(self):
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            password='password123'
        )
        self.leaderboard = Leaderboard.objects.create(
            user=self.user,
            total_score=1000,
            rank=1
        )
    
    def test_create_leaderboard(self):
        """리더보드 생성 테스트"""
        self.assertEqual(self.leaderboard.total_score, 1000)
        self.assertEqual(self.leaderboard.rank, 1)
    
    def test_leaderboard_str(self):
        """리더보드 문자열 표현 테스트"""
        expected_str = f"#{self.leaderboard.rank} {self.user.name} ({self.leaderboard.total_score} pts)"
        self.assertEqual(str(self.leaderboard), expected_str)


class UserAPITest(APITestCase):
    """사용자 API 테스트"""
    
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create(
            name='User 1',
            email='user1@example.com',
            password='password123'
        )
        self.user2 = User.objects.create(
            name='User 2',
            email='user2@example.com',
            password='password123'
        )
    
    def test_list_users(self):
        """사용자 목록 조회 테스트"""
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_user(self):
        """사용자 생성 API 테스트"""
        data = {
            'name': 'New User',
            'email': 'newuser@example.com',
            'password': 'password123'
        }
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
    
    def test_retrieve_user(self):
        """사용자 상세 조회 테스트"""
        response = self.client.get(f'/api/users/{self.user1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'User 1')


class TeamAPITest(APITestCase):
    """팀 API 테스트"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            password='password123'
        )
        self.team = Team.objects.create(
            name='Test Team',
            description='Test Description'
        )
        self.team.members.add(self.user)
    
    def test_list_teams(self):
        """팀 목록 조회 테스트"""
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_team(self):
        """팀 생성 API 테스트"""
        data = {
            'name': 'New Team',
            'description': 'New Team Description'
        }
        response = self.client.post('/api/teams/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ActivityAPITest(APITestCase):
    """활동 API 테스트"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            password='password123'
        )
        self.activity = Activity.objects.create(
            user=self.user,
            activity_type='Running',
            duration=30,
            calories_burned=300
        )
    
    def test_list_activities(self):
        """활동 목록 조회 테스트"""
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_activity(self):
        """활동 생성 API 테스트"""
        data = {
            'user': self.user.id,
            'activity_type': 'Swimming',
            'duration': 45,
            'calories_burned': 400
        }
        response = self.client.post('/api/activities/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class WorkoutAPITest(APITestCase):
    """운동 프로그램 API 테스트"""
    
    def setUp(self):
        self.client = APIClient()
        self.workout = Workout.objects.create(
            name='Test Workout',
            description='Test Description',
            exercises=['Exercise 1', 'Exercise 2'],
            difficulty_level='Medium'
        )
    
    def test_list_workouts(self):
        """운동 목록 조회 테스트"""
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_filter_by_difficulty(self):
        """난이도별 운동 필터링 테스트"""
        response = self.client.get('/api/workouts/by_difficulty/?difficulty=Medium')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LeaderboardAPITest(APITestCase):
    """리더보드 API 테스트"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            password='password123'
        )
        self.leaderboard = Leaderboard.objects.create(
            user=self.user,
            total_score=1000,
            rank=1
        )
    
    def test_list_leaderboard(self):
        """리더보드 목록 조회 테스트"""
        response = self.client.get('/api/leaderboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_top_users(self):
        """상위 사용자 조회 테스트"""
        response = self.client.get('/api/leaderboard/top_users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class APIRootTest(APITestCase):
    """API 루트 테스트"""
    
    def test_api_root(self):
        """API 루트 엔드포인트 테스트"""
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('teams', response.data)
        self.assertIn('activities', response.data)
        self.assertIn('workouts', response.data)
        self.assertIn('leaderboard', response.data)

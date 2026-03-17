from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Team, Activity, Workout, Leaderboard
from .serializers import UserSerializer, TeamSerializer, ActivitySerializer, WorkoutSerializer, LeaderboardSerializer

class StandardResultsSetPagination(PageNumberPagination):
    """표준 페이지네이션"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# ViewSets
class UserViewSet(viewsets.ModelViewSet):
    """사용자 ViewSet"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['created_at']
    search_fields = ['name', 'email']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['get'])
    def activities(self, request, pk=None):
        """사용자의 활동 조회"""
        user = self.get_object()
        activities = user.activities.all()
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)

class TeamViewSet(viewsets.ModelViewSet):
    """팀 ViewSet"""
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['created_at']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """팀 멤버 조회"""
        team = self.get_object()
        serializer = UserSerializer(team.members.all(), many=True)
        return Response(serializer.data)

class ActivityViewSet(viewsets.ModelViewSet):
    """활동 ViewSet"""
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'activity_type', 'date']
    search_fields = ['user__name', 'activity_type']
    ordering_fields = ['date', 'calories_burned', 'duration']
    ordering = ['-date']
    
    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """사용자별 활동 조회"""
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "user_id 매개변수 필요"}, status=status.HTTP_400_BAD_REQUEST)
        activities = Activity.objects.filter(user_id=user_id)
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)

class WorkoutViewSet(viewsets.ModelViewSet):
    """운동 프로그램 ViewSet"""
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['difficulty_level', 'created_at']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'difficulty_level', 'created_at']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def by_difficulty(self, request):
        """난이도별 운동 조회"""
        difficulty = request.query_params.get('difficulty')
        if not difficulty:
            return Response({"error": "difficulty 매개변수 필요"}, status=status.HTTP_400_BAD_REQUEST)
        workouts = Workout.objects.filter(difficulty_level=difficulty)
        serializer = WorkoutSerializer(workouts, many=True)
        return Response(serializer.data)

class LeaderboardViewSet(viewsets.ModelViewSet):
    """리더보드 ViewSet"""
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['team', 'rank']
    ordering_fields = ['rank', 'total_score']
    ordering = ['rank']
    
    @action(detail=False, methods=['get'])
    def top_users(self, request):
        """상위 사용자 조회"""
        limit = int(request.query_params.get('limit', 10))
        leaderboard = Leaderboard.objects.all()[:limit]
        serializer = LeaderboardSerializer(leaderboard, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """팀별 리더보드 조회"""
        team_id = request.query_params.get('team_id')
        if not team_id:
            return Response({"error": "team_id 매개변수 필요"}, status=status.HTTP_400_BAD_REQUEST)
        leaderboard = Leaderboard.objects.filter(team_id=team_id)
        serializer = LeaderboardSerializer(leaderboard, many=True)
        return Response(serializer.data)

# API Root
@api_view(['GET'])
def api_root(request):
    """API 루트 엔드포인트"""
    return Response({
        'users': request.build_absolute_uri('/api/users/'),
        'teams': request.build_absolute_uri('/api/teams/'),
        'activities': request.build_absolute_uri('/api/activities/'),
        'workouts': request.build_absolute_uri('/api/workouts/'),
        'leaderboard': request.build_absolute_uri('/api/leaderboard/'),
    })

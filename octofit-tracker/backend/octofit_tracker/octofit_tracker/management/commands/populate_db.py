from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'octofit_db 데이터베이스에 테스트 데이터를 입력합니다.'

    def handle(self, *args, **options):
        # Clear existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Leaderboard.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('기존 데이터를 삭제했습니다.'))

        # Create superhero users
        superhero_users = [
            {'name': 'Superman', 'email': 'superman@marvel.com', 'password': 'password123'},
            {'name': 'Batman', 'email': 'batman@dc.com', 'password': 'password123'},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'password': 'password123'},
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'password': 'password123'},
            {'name': 'Black Widow', 'email': 'blackwidow@marvel.com', 'password': 'password123'},
            {'name': 'Green Lantern', 'email': 'greenlantern@dc.com', 'password': 'password123'},
            {'name': 'Thor', 'email': 'thor@marvel.com', 'password': 'password123'},
            {'name': 'The Flash', 'email': 'theflash@dc.com', 'password': 'password123'},
        ]

        created_users = []
        for user_data in superhero_users:
            user = User.objects.create(**user_data)
            created_users.append(user)

        self.stdout.write(self.style.SUCCESS(f'{len(created_users)}명의 사용자를 생성했습니다.'))

        # Create teams
        marvel_team = Team.objects.create(
            name='Marvel Team',
            description='슈퍼히어로 마블 팀'
        )
        marvel_team.members.set(created_users[3:5])  # Iron Man, Black Widow

        dc_team = Team.objects.create(
            name='DC Team',
            description='슈퍼히어로 DC 팀'
        )
        dc_team.members.set([created_users[1], created_users[2], created_users[5]])  # Batman, Wonder Woman, Green Lantern

        self.stdout.write(self.style.SUCCESS('2개의 팀을 생성했습니다.'))

        # Create activities
        activity_types = ['Running', 'Swimming', 'Cycling', 'Gym', 'Yoga']
        now = datetime.now()
        for i, user in enumerate(created_users):
            for j in range(3):
                activity = Activity.objects.create(
                    user=user,
                    activity_type=activity_types[j % len(activity_types)],
                    duration=30 + j * 10,
                    calories_burned=200 + j * 50,
                    date=now - timedelta(days=j)
                )

        self.stdout.write(self.style.SUCCESS(f'{len(created_users) * 3}개의 활동을 생성했습니다.'))

        # Create workouts
        workouts_data = [
            {
                'name': 'Morning Cardio',
                'description': '아침 심장 운동',
                'exercises': ['Running', 'Jumping Jacks', 'Burpees'],
                'difficulty_level': 'Medium'
            },
            {
                'name': 'Strength Training',
                'description': '근력 운동',
                'exercises': ['Deadlifts', 'Squats', 'Bench Press'],
                'difficulty_level': 'Hard'
            },
            {
                'name': 'Yoga Session',
                'description': '요가 세션',
                'exercises': ['Downward Dog', 'Warrior Pose', 'Tree Pose'],
                'difficulty_level': 'Easy'
            },
        ]

        for workout_data in workouts_data:
            Workout.objects.create(**workout_data)

        self.stdout.write(self.style.SUCCESS(f'{len(workouts_data)}개의 운동 프로그램을 생성했습니다.'))

        # Create leaderboard entries
        for i, user in enumerate(created_users):
            if i < 5:
                team = marvel_team
            else:
                team = dc_team
            leaderboard = Leaderboard.objects.create(
                user=user,
                team=team,
                total_score=(i + 1) * 100,
                rank=i + 1
            )

        self.stdout.write(self.style.SUCCESS(f'{len(created_users)}개의 리더보드 항목을 생성했습니다.'))

        self.stdout.write(self.style.SUCCESS('✓ 테스트 데이터 적재 완료!'))

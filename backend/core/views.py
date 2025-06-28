from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile,Tasks
from .serializers import UserProfileSerializer, TasksSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import datetime
from .serializers import LeaderboardEntrySerializer
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"error": "Email and password required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    user_auth = authenticate(username=user.username, password=password)
    if user_auth is not None:
        return Response({
            "message": "Login successful",
            "username": user.username,  # ✅ Return username
            "email": user.email,
        }, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    return Response({"message": "User created successfully", "username": user.username}, status=status.HTTP_201_CREATED)

class TasksGetCreateView(generics.ListCreateAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
   # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
class TasksUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
   # permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()
from django.db.models import Sum
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from .models import Score
import datetime

from django.contrib import admin
from .models import UserScore

from django import forms
from .models import UserScore
from django.contrib.auth.models import User

# class UserScoreAdmin(admin.ModelAdmin):
#     list_display = ('user', 'daily_score', 'weekly_score', 'overall_score', 'last_updated_date')
#     list_display_links = ('user',)  # makes 'user' clickable
#     readonly_fields = ('last_updated_date',)

# def compute_ranking(queryset):
#     ranked = queryset.values('user__username') \
#         .annotate(total_points=Sum('points')) \
#         .order_by('-total_points')

#     return [
#         {'rank': idx + 1, 'username': entry['user__username'], 'points': entry['total_points']}
#         for idx, entry in enumerate(ranked)
#     ]

# @api_view(['GET'])
# def leaderboard_view(request):
#     now = timezone.now()
#     today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
#     week_start = today_start - datetime.timedelta(days=now.weekday())

#     username = request.GET.get('username')  # Client must pass ?username=yourname

#     daily_qs = Score.objects.filter(created_at__gte=today_start)
#     weekly_qs = Score.objects.filter(created_at__gte=week_start)
#     overall_qs = Score.objects.all()

#     daily = compute_ranking(daily_qs)
#     weekly = compute_ranking(weekly_qs)
#     overall = compute_ranking(overall_qs)

#     # Helper to get user's rank from ranking list
#     def get_user_rank(ranking, username):
#         for entry in ranking:
#             if entry['username'] == username:
#                 return entry
#         return {'rank': None, 'username': username, 'points': 0}

#     user_ranks = {
#         'daily': get_user_rank(daily, username),
#         'weekly': get_user_rank(weekly, username),
#         'overall': get_user_rank(overall, username),
#     }

    # return Response({
    #     'daily': LeaderboardEntrySerializer(daily, many=True).data,
    #     'weekly': LeaderboardEntrySerializer(weekly, many=True).data,
    #     'overall': LeaderboardEntrySerializer(overall, many=True).data,
    #     'user_ranks': user_ranks  # 💡 Add this to show user’s own rank
    # })

from django.utils.timezone import now
from datetime import timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import UserScore

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def update_user_score(request):
#     username = request.data.get('username')
#     #print(request.data)
#     new_overall = int(request.data.get('overall_score',0))
#    # print(f"hey broooo {username} {new_overall}")
#     try:
#         user = User.objects.get(username=username)
#     except User.DoesNotExist:
#         return Response({'error': 'User not found'}, status=404)
#     score_obj, created = UserScore.objects.get_or_create(user=user)

#     today = now().date()
#     last_update = score_obj.last_updated_date
#     score_diff = new_overall - score_obj.overall_score

#     if today != last_update:
#         # Reset daily score
#         score_obj.daily_score = 0

#         # Reset weekly score if week has changed
#         if today.isocalendar()[1] != last_update.isocalendar()[1]:
#             score_obj.weekly_score = 0

#     score_obj.daily_score += score_diff
#     score_obj.weekly_score += score_diff
#     score_obj.overall_score = new_overall
#     score_obj.last_updated_date = today

#     score_obj.save()

#     return Response({
#         'message': 'Score updated',
#         'daily_score': score_obj.daily_score,
#         'weekly_score': score_obj.weekly_score,
#         'overall_score': score_obj.overall_score
#     })
@api_view(['POST'])
@permission_classes([AllowAny])
def update_user_score(request):
    username = request.data.get('username')
    new_overall = int(request.data.get('overall_score', 0))

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    score_obj, created = UserScore.objects.get_or_create(user=user)

    today = timezone.now().date()

    # Set default for newly created scores
    if created:
        score_obj.last_updated_date = today
        score_obj.save()
    for score_obj in UserScore.objects.all():
        last_update = score_obj.last_updated_date
        if today != last_update:
            score_obj.daily_score = 0
            if today.isocalendar()[1] != last_update.isocalendar()[1]:
                score_obj.weekly_score = 0
            score_obj.last_updated_date = today
            score_obj.save()
    # last_update = score_obj.last_updated_date
    score_diff = new_overall - score_obj.overall_score

    # # Reset daily score if it's a new day
    # if today != last_update:
    #     score_obj.daily_score = 0

    #     # Reset weekly score if the week number has changed
    #     if today.isocalendar()[1] != last_update.isocalendar()[1]:
    #         score_obj.weekly_score = 0

    # Update scores
    score_obj.daily_score += score_diff
    score_obj.weekly_score += score_diff
    score_obj.overall_score = new_overall
    score_obj.last_score = score_obj.overall_score  # optional
    score_obj.last_updated_date = today
    score_obj.save()

    return Response({
        'message': 'Score updated',
        'daily_score': score_obj.daily_score,
        'weekly_score': score_obj.weekly_score,
        'overall_score': score_obj.overall_score
    })

    from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserScore

@api_view(['GET'])
def leaderboard_view(request):
    username = request.GET.get('username')

    def compute_ranking(userscore_list, field):
        sorted_scores = sorted(userscore_list, key=lambda x: getattr(x, field), reverse=True)
        ranking = []
        for idx, entry in enumerate(sorted_scores, start=1):
            ranking.append({
                'rank': idx,
                'username': entry.user.username,
                'points': getattr(entry, field)
            })
        return ranking

    def get_user_rank(ranking, username):
        for entry in ranking:
            if entry['username'] == username:
                return entry
        return {'rank': None, 'username': username, 'points': 0}

    scores = UserScore.objects.select_related('user').all()

    daily = compute_ranking(scores, 'daily_score')
    weekly = compute_ranking(scores, 'weekly_score')
    overall = compute_ranking(scores, 'overall_score')

    user_ranks = {
        'daily': get_user_rank(daily, username),
        'weekly': get_user_rank(weekly, username),
        'overall': get_user_rank(overall, username),
    }

    return Response({
        'daily': daily,
        'weekly': weekly,
        'overall': overall,
        'user_ranks': user_ranks
    })


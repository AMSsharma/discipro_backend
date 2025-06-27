from django.urls import path
from .views import register_user, TasksGetCreateView, TasksUpdateDeleteView, login_user, update_user_score, leaderboard_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('register/', register_user, name='register'),
    #path('leaderboard/', leaderboard_view, name='leaderboard'),
    path('login/', login_user, name='login_user'),
    path('logout', TokenRefreshView.as_view(), name='token_refresh'),
    path('',TasksGetCreateView.as_view()),
    path('<int:pk>/', TasksUpdateDeleteView.as_view()),
    path('update-score/', update_user_score, name='update_score'),
    path('leaderboard/', leaderboard_view, name='leaderboard'),
]
 
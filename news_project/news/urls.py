from django.urls import path
from .views import NewsListView, NewsDetailView, LikeNewsView, RegisterView
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('news/', NewsListView.as_view(), name='news-list'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news-detail'),
    path('news/<int:news_id>/like/', LikeNewsView.as_view(), name='like-news'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', ObtainAuthToken.as_view(), name='login'),
]

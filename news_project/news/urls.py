from django.urls import path
from .views import (
    NewsListView, NewsDetailView, LikeNewsView, NewsByTagView, NewsStatsView, register_view, login_view, logout_view
)
from django.shortcuts import render
from .models import News, Tag

def news_list_view(request):
    return render(request, 'news_list.html', {'news_list': News.objects.all()})

def news_detail_view(request, pk):
    news = News.objects.get(pk=pk)
    news.views += 1
    news.save()
    return render(request, 'news_detail.html', {'news': news})

def news_by_tag_view(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    news_list = tag.news.all()
    return render(request, 'news_by_tag.html', {'news_list': news_list, 'tag': tag})

def news_stats_view(request):
    news_list = News.objects.all().order_by('-views')
    return render(request, 'news_stats.html', {'news_list': news_list})

urlpatterns = [
    path('', news_list_view, name='news-list'),
    path('news/<int:pk>/', news_detail_view, name='news-detail'),
    path('news/tag/<int:tag_id>/', news_by_tag_view, name='news-by-tag'),
    path('news/stats/', news_stats_view, name='news-stats'),
    path('news/<int:news_id>/like/', LikeNewsView.as_view(), name='like-news'),
]

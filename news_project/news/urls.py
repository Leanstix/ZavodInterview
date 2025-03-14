from django.urls import path
from .models import News, Tag, Like
from .views import (
    NewsListView, NewsDetailView, LikeNewsView, RegisterView, LoginView, LogoutView, NewsListCreateView, NewsDeleteView
)
from django.shortcuts import render
from .models import News, Tag
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Count

def news_list_view(request):
    page = int(request.GET.get('page', 1))
    per_page = 5 if page == 1 else 3 
    
    news_list = News.objects.prefetch_related('tags').all().order_by('-created_at')
    paginator = Paginator(news_list, per_page)

    try:
        news_page = paginator.page(page)
    except:
        return JsonResponse({'news': []})  

    news_data = [
        {
            'id': news.id,
            'title': news.title,
            'text': news.text[:150] + "...",
            'tags': [{'id': tag.id, 'name': tag.name} for tag in news.tags.all()] 
        } for news in news_page
    ]

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  
        return JsonResponse({'news': news_data})

    return render(request, 'news/news_list.html', {'news_list': news_list})  

def register_view(request):
    return render(request, 'news/register.html')


def news_detail_view(request, pk):
    news = get_object_or_404(News, pk=pk)
    news.views += 1
    news.save()

    like_count = news.like_set.filter(is_like=True).count() 

    return render(request, 'news/news_detail.html', {'news': news, 'like_count': like_count})

def news_by_tag_view(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    page = int(request.GET.get('page', 1))
    per_page = 5 if page == 1 else 3  
    news_list = tag.news.all().order_by('-created_at')
    paginator = Paginator(news_list, per_page)

    try:
        news_page = paginator.page(page)
    except:
        return JsonResponse({'news': []})  

    news_data = [
        {
            'id': news.id,
            'title': news.title,
            'text': news.text[:150] + "...",
        } for news in news_page
    ]
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  
        return JsonResponse({'news': news_data})

    return render(request, 'news/news_by_tag.html', {'tag': tag, 'news_list': news_data})

def news_stats_view(request):
    news_list = News.objects.annotate(like_count=Count('like')).order_by('-views')  
    return render(request, 'news/news_stats.html', {'news_list': news_list})

def login_view(request):
    return render(request, 'news/login.html')

urlpatterns = [
    # Frontend views
    path('', news_list_view, name='news-list'),
    path('news/<int:pk>/', news_detail_view, name='news-detail'),
    path('news/tag/<int:tag_id>/', news_by_tag_view, name='news-by-tag'),
    path('news/stats/', news_stats_view, name='news-stats'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('news/stats/', news_stats_view, name='news-stats'),

    # API views
    
    path('api/news/<int:pk>/', NewsDetailView.as_view(), name='news-api-detail'),
    path('api/news/<int:news_id>/like/', LikeNewsView.as_view(), name='like-news'),
    path('api/news/', NewsListCreateView.as_view(), name='news-list-create'),
    path('api/news/<int:news_id>/delete/', NewsDeleteView.as_view(), name='news-delete'),

    # Authentication views
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
]

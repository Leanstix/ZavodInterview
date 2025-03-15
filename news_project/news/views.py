from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import News, Like
from .serializers import NewsSerializer, LikeSerializer, TagSerializer
from django.shortcuts import render

class NewsListView(generics.ListAPIView):
    queryset = News.objects.all().order_by('-created_at')[:5]
    serializer_class = NewsSerializer

class NewsDetailView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        return super().retrieve(request, *args, **kwargs)

class LikeNewsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, news_id):
        news = get_object_or_404(News, id=news_id)
        like, created = Like.objects.get_or_create(user=request.user, news=news)

        if created:
            like.is_like = True 
        else:
            like.is_like = not like.is_like 

        like.save()

        like_count = news.like_set.filter(is_like=True).count() 

        return Response({'likes': like_count, 'liked': like.is_like}, status=status.HTTP_200_OK)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if User.objects.filter(username=username).exists():
            return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

class NewsListCreateView(generics.ListCreateAPIView):
    queryset = News.objects.all().order_by('-created_at')
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  

    def perform_create(self, serializer):
        serializer.save()

class NewsDeleteView(APIView):
    permission_classes = [IsAdminUser] 

    def delete(self, request, news_id):
        news = get_object_or_404(News, id=news_id)
        news.delete()
        return Response({"message": "News deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if not user.is_active:
                return Response({'error': 'User account is disabled'}, status=status.HTTP_403_FORBIDDEN)
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete() 
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

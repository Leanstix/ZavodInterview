from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import News, Like
from .serializers import NewsSerializer, LikeSerializer

class NewsListView(generics.ListAPIView):
    queryset = News.objects.all().order_by('-created_at')
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
        news = News.objects.get(id=news_id)
        like, created = Like.objects.get_or_create(user=request.user, news=news)
        like.is_like = not like.is_like  # Toggle like/dislike
        like.save()
        return Response({'likes': news.like_set.filter(is_like=True).count()})
    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        if User.objects.filter(username=username).exists():
            return Response({"error": "User already exists"}, status=400)
        user = User.objects.create_user(username=username, password=password)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

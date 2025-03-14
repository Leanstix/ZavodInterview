from rest_framework import serializers
from .models import News, Tag, Like

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class NewsSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ['id', 'title', 'text', 'image', 'tags', 'created_at', 'views', 'likes_count']

    def get_likes_count(self, obj):
        return obj.like_set.filter(is_like=True).count()

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username') 

    class Meta:
        model = Like
        fields = ['id', 'user', 'news', 'is_like']

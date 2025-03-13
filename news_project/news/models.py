from django.contrib.auth.models import User
from django.db import models

class News(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    tags = models.ManyToManyField('Tag', related_name='news')
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True) 

    class Meta:
        unique_together = ('user', 'news') 

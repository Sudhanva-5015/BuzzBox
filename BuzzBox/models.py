from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_user = models.IntegerField(null=False)
    profile_img = models.ImageField(upload_to='profile_images', default='default.png')
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.user.username
class Post(models.Model):
    id= models.UUIDField(primary_key = True , default =uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image= models.ImageField(upload_to= 'post_images')
    caption= models.TextField()
    posted_on= models.DateField(default=datetime.now)
    no_of_likes = models.IntegerField(default = 0)
    
    def __str__(self):
        return f"Post by {self.user.username}"
    
class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)
  
    def __str__(self):
        return self.username
    
class FollowersCount(models.Model):
    follower = models.CharField(max_length = 100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user
        

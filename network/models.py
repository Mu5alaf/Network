from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime,date

class User(AbstractUser):
    pass

#creating post models#
class New_Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="writer",default=True)
    content = models.TextField(max_length=150)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    def __str__(self):
        return f" Post {self.id} Create by {self.user} on {self.date:'%Y-%m-%d at %H:%M'}"
#creating followers model
class followers_dashboard(models.Model):
    follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name="Following")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="followed")
    def __str__(self):
        return f"{self.user} is following {self.follower}"
    
class LikesModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserLike')
    post = models.ForeignKey(New_Post, on_delete=models.CASCADE, related_name='postLiked')
    def __str__(self):
        return f'{self.user} liked this {self.post}'
    
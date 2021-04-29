from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Posts(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    time = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name = 'likes',blank = True)
    Comments = models.ManyToManyField(User, related_name = 'Comments', blank = True)

    class Meta:
       ordering = ['-time']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('addPost')

    def total_likes(self):
        return self.likes.all().count()

    def total_comments(self):
        return self.comments_set.all().count()


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
  
    
    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    text = models.TextField(blank = True, null = True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.text)
    
    class Meta:
       ordering = ['-date']

    
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    image = models.ImageField(null=True,blank=True,default = 'images/profile_pics/default_profile_pic.png',upload_to = 'images/profile_pics')
    bio = models.TextField(blank=True,default='Your bio here...')
    fullname = models.CharField(max_length = 100, null=True, default="",blank=True)
    followers = models.ManyToManyField(User, blank =True, related_name="followers")
            
    def __str__(self):
        return str(self.user)

    def total_followers(self):
        return self.followers.all().count()


FOLLOW_CHOICES = (
    ('Follow', 'Follow'),
    ('Following', 'Following'),
)

class Follow(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    value = models.CharField(choices=FOLLOW_CHOICES, max_length=10)
  
    def __str__(self):
        return f"{self.user}-{self.profile}-{self.value}"


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:     
        Profile.objects.create(user=instance)
    instance.profile.save()



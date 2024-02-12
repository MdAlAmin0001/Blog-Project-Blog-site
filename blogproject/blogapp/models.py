from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils import timezone

def profile_image_upload_path(instance, filename):
    # ফাইলটি ব্যবহারকারীর নাম ভিত্তিক একটি ফোল্ডারে আপলোড করো
    return f"media/profileimage/{instance.username}/{timezone.now().strftime('%Y%m%d%H%M%S')}-{filename}"

# Create your models here.

class Custom_User(AbstractUser):
    USER=[
        ('user','User'),('blogger','Blogger'),('admin','Admin'),
        
    ]
    
    display_name=models.CharField(max_length=100)
    email=models.EmailField()
    password=models.CharField(max_length=100)
    user_type=models.CharField(choices=USER, max_length=120)
    profile_image = models.ImageField(upload_to=profile_image_upload_path, null=True)
    otp_token = models.CharField(max_length = 6, blank = True, null = True)
    
    
    
    def __str__(self):
        return self.display_name


class BlogPost(models.Model):
    Created_By=models.ForeignKey(Custom_User, on_delete=models.CASCADE, null=True)
    Create_at=models.DateTimeField(auto_now_add=True, null=True)
    Post_Image=models.ImageField(upload_to="media/postimages", null=True)
    Post_Title=models.CharField(max_length=100)
    Post_Description=models.TextField(max_length=5000) 
    Permission=models.BooleanField(default=False)
    see_more=models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.Post_Title
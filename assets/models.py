from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    studentID = models.IntegerField(default=0)
    branch = models.CharField(max_length=20, default='Dorset College')
    year = models.CharField(max_length=20, default='First Year')
    phone_no = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class RequestInfo(models.Model):
    Item_info = models.CharField(max_length=150)
    Description = models.CharField(max_length=150)
    Location = models.CharField(max_length=100)
    the_date = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='media/', blank=True)

    def __str__(self):
        return self.Item_info


class Claim(models.Model):
    item = models.ForeignKey(RequestInfo, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

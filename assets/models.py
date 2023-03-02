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


class ItemData(models.Model):
    itemID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    Item_info = models.CharField(default="", max_length=150)
    Description = models.CharField(default="", max_length=150)
    Location = models.CharField(default="", max_length=100)

    def __str__(self):
        return self.title


class RequestInfo(models.Model):
    Item_info = models.CharField(max_length=150)
    Description = models.CharField(max_length=150)
    Location = models.CharField(max_length=100)

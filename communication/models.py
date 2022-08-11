from django.db import models
from users.models import *
# Create your models here.
class Announcement(models.Model):
    title=models.CharField(max_length=300, unique=True)
    body = models.TextField()
    author = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    date_posted=models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    REQUIRED_FIELDS=[title, body , author, course]

class Reply(models.Model):
    author = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    body = models.TextField()
    date_posted=models.DateTimeField(auto_now_add=True)
    announcement=models.ForeignKey(Announcement, on_delete=models.CASCADE)

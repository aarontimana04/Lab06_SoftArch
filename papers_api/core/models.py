from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
class Author(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    bio = models.TextField(blank=True, default='')
    institute = models.CharField(max_length=120, blank=True)
    def __str__(self): return self.name
class Paper(models.Model):
    title = models.CharField(max_length=200)
    abstract = models.TextField(blank=True, default='')
    url = models.URLField(blank=True)
    category = models.CharField(max_length=80, blank=True)
    keywords = models.CharField(max_length=250, blank=True)
    authors = models.ManyToManyField(Author, related_name='papers')
    downloads = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subs')
    status = models.CharField(max_length=20, default='TRIAL') # TRIAL, ACTIVE, CANCELED, EXPIRED
    started_at = models.DateTimeField(auto_now_add=True)
    auto_renew = models.BooleanField(default=False)
class Log(models.Model):
    level = models.CharField(max_length=10, default='INFO')
    event = models.CharField(max_length=120)
    details = models.TextField(blank=True, default='')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    paper = models.ForeignKey(Paper, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

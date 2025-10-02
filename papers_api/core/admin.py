from django.contrib import admin
from .models import Author, Paper, Subscription, Log
admin.site.register(Author)
admin.site.register(Paper)
admin.site.register(Subscription)
admin.site.register(Log)

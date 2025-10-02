from rest_framework import serializers
from .models import Author, Paper, Subscription, Log
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id','name','email','bio','institute']
class PaperSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    author_ids = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), many=True, write_only=True, source='authors')
    class Meta:
        model = Paper
        fields = ['id','title','abstract','url','category','keywords','authors','author_ids','downloads','created_at']
class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id','status','started_at','auto_renew']
class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ['id','level','event','details','user','paper','created_at']

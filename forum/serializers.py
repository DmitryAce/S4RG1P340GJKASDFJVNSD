from rest_framework import serializers
from .models import Forum, Post, Rating, GlobalRating
from django.contrib.auth import get_user_model

User = get_user_model()


class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'avatar']
        
class GlobalRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalRating
        fields = ['user', 'rating']

from django.contrib import admin
from .models import CustomUser, Forum, Post, Rating, GlobalRating

# Регистрируем модели
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'bio')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active', 'is_superuser')

@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'forum', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'updated_at', 'forum')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'score')
    list_filter = ('score',)
    search_fields = ('user__username', 'post__title')

@admin.register(GlobalRating)
class GlobalRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating')
    search_fields = ('user__username',)

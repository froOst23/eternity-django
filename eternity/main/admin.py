from django.contrib import admin
from .models import Post, Profile, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'date')
    search_fields = ('id', 'date', 'title', 'content')
    list_filter = ('id', 'author', 'date')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created', 'is_online')
    search_fields = ('id', 'user', 'created')
    list_filter = ('id', 'user', 'created', 'is_online')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post', 'updated')
    search_fields = ('id', 'author', 'post')
    list_filter = ('id', 'author', 'post', 'updated')

admin.site.register(Post, PostAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Comment, CommentAdmin)
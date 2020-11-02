from django.contrib import admin
from .models import Post, Profile, Comment, PostLike

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'date')
    search_fields = ('title', 'tag')
    list_filter = ('author', 'date')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created', 'is_online')
    search_fields = ('user', 'created')
    list_filter = ('user', 'created', 'is_online')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post', 'updated')
    # search_fields = ('author', 'post')
    list_filter = ('author', 'post')


class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user')
    # search_fields = ('id', 'post', 'user')
    list_filter = ('post',)

admin.site.register(Post, PostAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(PostLike, PostLikeAdmin)
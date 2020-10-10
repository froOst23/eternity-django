from django import template
from main.models import Comment

register = template.Library()

@register.simple_tag(name='comment_count')
def comment_cnt(post_title):
    return Comment.objects.filter(post__title=post_title).count()
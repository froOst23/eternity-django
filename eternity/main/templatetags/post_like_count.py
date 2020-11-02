from django import template
from main.models import PostLike

register = template.Library()

@register.simple_tag(name='post_like_count')
def like_cnt(post_like):
    return PostLike.objects.filter(post__title=post_like).count()
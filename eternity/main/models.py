from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.forms import User
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(verbose_name='Название', max_length=100)
    tag = models.CharField(verbose_name='Тег', max_length=100, blank=True)
    content = models.TextField(verbose_name='Содержание статьи', max_length=10000, blank=True)
    date = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True)
    image = models.FileField(verbose_name='Изображение', validators=[FileExtensionValidator(['png', 'jpeg', 'jpg', 'gif'])], blank=True, null=True)

    class Meta():
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    # корректирует отображение в административной панели название записи
    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return f'/post/{self.id}'


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Понравившийся пост')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Кто лайкнул')

    class Meta():
        verbose_name = 'Лайк поста'
        verbose_name_plural = 'Лайки постов'

    def __str__(self):
        return f'{self.post}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Комментируемый пост')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    content = models.TextField(verbose_name='Содержание', max_length=500)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_changed = models.BooleanField(default=False, verbose_name='Коммент был изменен')
    is_reply = models.BooleanField(default=False, verbose_name='Был сделан ответ')
    reply_to = models.CharField(verbose_name='Кому сделан ответ (author username)', max_length=100, null=True, blank=True)
    reply_id = models.PositiveIntegerField(verbose_name='Кому сделан ответ (author id)', null=True, blank=True)
    parent = models.PositiveIntegerField(verbose_name='Ответ на комментарий (id)', null=True, blank=True)

    class Meta():
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{str(self.post)} {str(self.author)}'


# Расширяем модель User с помощью связи user - "один-к-одному"
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    bio = models.TextField(max_length=200, verbose_name='О себе', blank=True)
    photo = models.FileField(verbose_name='Изображение', validators=[FileExtensionValidator(['png', 'jpeg', 'jpg'])], blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    is_online = models.BooleanField(default=False, verbose_name='Сейчас на сайте?')

    class Meta():
        verbose_name = 'Расширение модели User'
        verbose_name_plural = 'Расширения модели User'

    def __str__(self):
        return f'{str(self.user)}'

    def get_absolute_url(self):
        return f'/accounts/profile/id{self.id}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

from .models import Post, Profile, Comment, PostLike
from .forms import NewPostForm, LoginPostForm, RegisterPostForm, UpdateUserForm, ProfileUpdateForm, CommentCreateForm
from django.shortcuts import render, redirect
from django.db import transaction
from django.dispatch import receiver  
from django.views.generic import DetailView, DeleteView, UpdateView, CreateView
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView, reverse_lazy
from django.contrib.auth.forms import User, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.http import HttpResponseRedirect, HttpResponse
from django.core.files.uploadhandler import FileUploadHandler

class PostDetailView(DetailView):
    model = Post
    template_name = 'main/detail_view.html'
    context_object_name = 'detail_post'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.all()
        context['comment'] = Comment.objects.all()
        return context
    

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'main/update_post.html'
    form_class = NewPostForm
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].author:
            messages.error(self.request, f'Недостаточно прав для изменения')
            return self.handle_no_permission()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)
        context['post'] = Post.objects.all()
        # передаем параметр next (возвращение на предыдущую страницу) чтобы использовать в форме
        context['next_url'] = self.request.GET.get('next')
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        messages.success(self.request, 'Пост успешно изменен')
        return next_url


class PostAddView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'main/add_post.html'
    form_class = NewPostForm
    success_url = reverse_lazy('home')

    def image(request):
        image_file = request.FILES['image_file'].file.read()
        Post.objects.create(image=image_file)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        messages.success(self.request, f'Пост успешно добавлен')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, f'Произошла ошибка заполнения формы')
        return super(PostAddView, self).form_invalid(form)  
    

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'main/delete_post.html'
    form_class = NewPostForm
    success_url = reverse_lazy('home')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.author:
            messages.error(self.request, f'Недостаточно прав для удаления')
            return self.handle_no_permission()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(self.request, f'Пост успешно удален')
        return HttpResponseRedirect(success_url)


class LoginPostView(LoginView):
    model = Profile
    template_name = 'main/auth.html'
    form_class = LoginPostForm
    success_url = reverse_lazy('home')

    def form_invalid(self, form):
        messages.error(self.request, f'Неверный логин или пароль')
        return super(LoginPostView, self).form_invalid(form)

    def get_success_url(self):
        messages.info(self.request, f'Авторизация выполнена')
        return self.success_url

class LogoutPostView(LogoutView):
    def get_next_page(self):
        next_page = reverse_lazy('home')
        messages.info(self.request, f'Выход из системы')
        return next_page


class RegisterPostView(CreateView):
    model = User
    template_name = 'main/registration.html'
    form_class = RegisterPostForm
    success_url = reverse_lazy('home')

    # при успешной регистрации пользователя входим в систему
    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        auth_user = authenticate(username=username, password=password)
        messages.success(self.request, f'Пользователь {username} успешно создан')
        login(self.request, auth_user)
        return form_valid


class UserDetailView(DetailView):
    model = Profile
    template_name = 'main/profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['post'] = Post.objects.all()
        context['profile'] = Profile.objects.all()
        return context


"""
@login_required
Если пользователь не авторизован, то перенаправляет его на URL, указанный в параметре конфигурации 
settings.LOGIN_URL, передавая текущий абсолютный путь в запросе.
https://djbook.ru/rel1.8/topics/auth/default.html

@transaction.atomic
Django предоставляет один API для управления транзакциями базы данных.
Атомарность является основным свойством транзакций базы данных. atomic позволяет создать блок кода, 
для которого гарантируется атомарность операций над базой данных. Если этот блок кода выполнился без ошибок, 
все изменения фиксируются в базе данных. Если произошла ошибка, все изменений будут отменены.
https://djbook.ru/rel1.7/topics/db/transactions.html
"""
@login_required
@transaction.atomic
def update_profile(request, pk):
    next_url = request.GET.get('next')
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Профиль успешно обновлен'))
            return redirect(next_url)
        else:
            messages.error(request, ('Произошла ошибка заполнения формы'))
    # request.FILES - ожидаем загрузки файла на сервер
    elif request.method == 'FILES':
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # FileUploadHandler используем для загрузки файла на сервер
            FileUploadHandler(request.FILES['photo'])
            messages.success(request, ('Профиль успешно обновлен'))
            return redirect(next_url)
        else:
            messages.error(request, ('Произошла ошибка заполнения формы'))
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'main/profile_settings.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def add_comment(request, pk):
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            # указываем текущего авторизованного пользователя
            comment.author = request.user
            # указываем текущий пост
            comment.post = Post.objects.get(id=pk)
            # делаем запись в бд
            comment.save()
            messages.success(request, 'Комментарий добавлен')
            return redirect(f'/post/{pk}')
        else:
            messages.error(request, 'Произошла ошибка заполнения формы')
    else:
        form = CommentCreateForm(request.POST)
    return render(request, 'main/add_comment.html', {'form': form})


@login_required
def reply_comment(request, pk, parent_id, reply_to, reply_id):
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            # указываем текущего авторизованного пользователя
            comment.author = request.user
            # указывает что коммент был ответом
            comment.is_reply = True
            # указываем текущий пост
            comment.parent = int(parent_id)
            # указываем кому ответили
            comment.reply_to = str(reply_to)
            comment.reply_id = int(reply_id)
            comment.post = Post.objects.get(id=pk)
            # делаем запись в бд
            comment.save()
            messages.success(request, 'Комментарий добавлен')
            return redirect(f'/post/{pk}')
        else:
            messages.error(request, 'Произошла ошибка заполнения формы')
    else:
        form = CommentCreateForm(request.POST)
    return render(request, 'main/reply_comment.html', {'form': form})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = 'main/update_comment.html'
    form_class = CommentCreateForm
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].author:
            messages.error(self.request, f'Недостаточно прав для удаления')
            return self.handle_no_permission()
        return kwargs

    # передаем параметр next (возвращение на предыдущую страницу) чтобы использовать в форме
    def get_context_data(self, **kwargs):
        context = super(CommentUpdateView, self).get_context_data(**kwargs)
        context['next_url'] = self.request.GET.get('next')
        return context
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        messages.success(self.request, 'Комментарий успешно изменен')
        return next_url

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_changed = True
        self.object.save()
        return super().form_valid(form)
    

class DeleteCommentView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'main/delete_comment.html'
    form_class = CommentCreateForm

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.author:
            messages.error(self.request, f'Недостаточно прав для удаления')
            return self.handle_no_permission()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(self.request, f'Комментарий успешно удален')
        return HttpResponseRedirect(success_url)
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url

    def get_context_data(self, **kwargs):
        context = super(DeleteCommentView, self).get_context_data(**kwargs)
        context['next_url'] = self.request.GET.get('next')
        return context


def index(request):
    post = Post.objects.order_by('-date')
    profile = Profile.objects.order_by('-id')
    return render(request, 'main/index.html', {'post': post, 'profile': profile})


"""
Используем простой фильтр по нашей базе данных
https://django.fun/docs/django/ru/3.0/topics/db/queries/
"""
def tag(request, pk):
    filter_object = Post.objects.filter(tag__icontains=str(pk))
    post = Post.objects.filter(tag__icontains=str(pk))
    profile = Profile.objects.all()
    messages.info(request, (f'Поиск по тегу "{pk}" выполнен'))
    return render(request, 'main/index.html', {'post': post, 'profile': profile})


@login_required
def post_likes(request, pk):
    # Если у поста есть лайк...
    if PostLike.objects.filter(post=Post.objects.get(id=pk)).exists():
        # Если текущий пользователь уже лайкнул пост, то удаляем запись о лайке
        if PostLike.objects.filter(post=Post.objects.get(id=pk), user=request.user).exists():
            PostLike.objects.filter(post=Post.objects.get(id=pk), user=request.user).delete()
        # Иначе создаем запись о лайке
        else:
            PostLike.objects.create(post=Post.objects.get(id=pk), user=request.user)
    else:
        # Если записи о лайке поста не существует - создаем запись с текущим пользователем
        PostLike.objects.create(post=Post.objects.get(id=pk), user=request.user)
    return redirect('home')


@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):    
    user.profile.is_online = True
    user.profile.save()

@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):   
    user.profile.is_online = False
    user.profile.save()


def check_user_name(request):
    if request.method == 'GET':
        user_name = request.GET["user_name"]
        print(user_name)
        return HttpResponse('ok', content_type='text/html')
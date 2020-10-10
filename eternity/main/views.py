from django.shortcuts import render, redirect
from .models import Post, Profile, Comment
from .forms import NewPostForm, LoginPostForm, RegisterPostForm, UpdateUserForm, ProfileUpdateForm, CommentCreateForm
from django.views.generic import DetailView, DeleteView, UpdateView, CreateView
from django.contrib.auth.views import LoginView, LogoutView, reverse_lazy
from django.contrib.auth.forms import User, UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.contrib import messages
from django.core.files.uploadhandler import FileUploadHandler
from django.contrib.messages.views import SuccessMessageMixin

class PostDetailView(DetailView):
    model = Post
    template_name = 'main/detail_view.html'
    context_object_name = 'detail_post'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['photo'] = Profile.objects.all()
        context['comment'] = Comment.objects.all()
        return context
    

class PostUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'main/update-post.html'
    form_class = NewPostForm
    success_message = 'Пост успешно изменен'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].author:
            return self.handle_no_permission()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)
        context['post'] = Post.objects.all()
        return context


class PostAddView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'main/add-post.html'
    form_class = NewPostForm
    success_url = reverse_lazy('home')
    success_message = 'Пост успешно добавлен'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)
    

class PostDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'main/delete-post.html'
    form_class = NewPostForm
    success_url = reverse_lazy('home')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.author:
            messages.error(self.request, 'Недостаточно прав для удаления')
            return self.handle_no_permission()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(self.request, 'Пост успешно удален')
        return HttpResponseRedirect(success_url)


class LoginPostView(SuccessMessageMixin, LoginView):
    template_name = 'main/auth.html'
    form_class = LoginPostForm
    success_url = reverse_lazy('home')
    success_message = 'Успешная авторизация'

    def get_success_url(self):
        return self.success_url


class LogoutPostView(SuccessMessageMixin, LogoutView):
    def get_next_page(self):
        next_page = reverse_lazy('home')
        messages.success(self.request, f'Выход из системы')
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


# # Устаревшая функция - необходимо убрать
# class UpdateUserView(LoginRequiredMixin, UpdateView):
#     model = User
#     template_name = 'main/profile_main.html'
#     form_class = UpdateUserForm

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         if str(self.request.user) != str(kwargs['instance'].username):
#             return self.handle_no_permission()
#         return kwargs


# # Устаревшая функция - необходимо убрать
# class ProfileUpdateView(LoginRequiredMixin, UpdateView):
#     model = Profile
#     template_name = 'main/profile_extra.html'
#     form_class = ProfileUpdateForm
#     second_form_class = UpdateUserForm

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         if self.request.user != kwargs['instance'].user:
#             return self.handle_no_permission()
#         return kwargs

#     def get_context_data(self, **kwargs):
#         context = super(ProfileUpdateView, self).get_context_data(**kwargs)
#         context['profile'] = Profile.objects.all()
#         return context


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
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Профиль успешно обновлен'))
            # return redirect('home')
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
        else:
            messages.error(request, ('Произошла ошибка заполнения формы'))
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'main/profile_settings.html', {'user_form': user_form, 'profile_form': profile_form})


def index(request):
    post = Post.objects.order_by('-date')
    profile = Profile.objects.order_by('-id')
    # cnt_comment = Comment.objects.filter(post__title='')
    return render(request, 'main/index.html', {'post': post, 'profile': profile})

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
            return redirect(f'/post/{pk}')
    else:
        form = CommentCreateForm(request.POST)
    return render(request, 'main/add-comment.html', {'form': form})


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


def about(request):
    return render(request, 'main/about.html')

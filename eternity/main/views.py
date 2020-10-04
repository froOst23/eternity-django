from django.shortcuts import render, redirect
from .models import Post, Profile
from .forms import NewPostForm, LoginPostForm, RegisterPostForm, UpdateUserForm, ProfileUpdateForm
from django.views.generic import DetailView, DeleteView, UpdateView, CreateView
from django.contrib.auth.views import LoginView, LogoutView, reverse_lazy
from django.contrib.auth.forms import User, UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

class PostDetailView(DetailView):
    model = Post
    template_name = 'main/detail_view.html'
    context_object_name = 'detail_post'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['photo'] = Profile.objects.all()
        return context
    

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'main/update-post.html'
    form_class = NewPostForm
    success_url = reverse_lazy('home')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].author:
            return self.handle_no_permission()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)
        context['post'] = Post.objects.all()
        return context


class PostAddView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'main/add-post.html'
    form_class = NewPostForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)
    

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'main/delete-post.html'
    form_class = NewPostForm
    success_url = reverse_lazy('home')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.author:
            return self.handle_no_permission()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class LoginPostView(LoginView):
    template_name = 'main/auth.html'
    form_class = LoginPostForm
    success_url = reverse_lazy('home')

    def get_success_url(self):
        return self.success_url


class LogoutPostView(LogoutView):
    next_page = reverse_lazy('home')


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
        login(self.request, auth_user)
        return form_valid


class UpdateUserView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'main/profile_main.html'
    form_class = UpdateUserForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if str(self.request.user) != str(kwargs['instance'].username):
            return self.handle_no_permission()
        return kwargs


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'main/profile_extra.html'
    form_class = ProfileUpdateForm
    second_form_class = UpdateUserForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].user:
            return self.handle_no_permission()
        return kwargs


class UserDetailView(DetailView):
    model = Profile
    template_name = 'main/profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['post'] = Post.objects.all()
        return context


def index(request):
    post = Post.objects.order_by('-date')
    profile = Profile.objects.order_by('-id')
    return render(request, 'main/index.html', {'post': post, 'profile': profile})


def about(request):
    return render(request, 'main/about.html')

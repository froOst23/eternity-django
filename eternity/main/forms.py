from .models import Post, Profile, Comment
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea, PasswordInput, FileInput
from django.contrib.auth.forms import AuthenticationForm, User

class NewPostForm(ModelForm):
    # указываем с какой моделью будем работтать и какими полями модели
    class Meta:
        model = Post
        fields = ['title', 'tag', 'content', 'image']

    # задаем класс формы и атрибут placeholder
    def __init__(self, *args, **kwargs):
        super(NewPostForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget = TextInput(attrs={'class': 'post-form-input font-nunito-regular-normal', 'placeholder': 'Название поста'})
        self.fields['title'].label = False
        self.fields['tag'].widget = TextInput(attrs={'class': 'post-form-input font-nunito-regular-normal', 'placeholder': 'Используемые теги'})
        self.fields['tag'].label = False
        self.fields['content'].widget = Textarea(attrs={'class': 'post-form-input-textarea font-nunito-regular-normal', 'placeholder': 'Описание поста'})
        self.fields['content'].label = False
        self.fields['image'].widget = FileInput(attrs={'class': 'post-form-input font-nunito-regular-normal', 'placeholder': 'Фото поста'})
        self.fields['image'].label = False


class LoginPostForm(AuthenticationForm, ModelForm):
    # указываем с какой моделью будем работтать и какисми полями модели
    class Meta:
        model = User
        fields = ['username', 'password']

    # задаем класс формы и атрибут placeholder
    def __init__(self, *args, **kwargs):
        super(LoginPostForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = TextInput(attrs={'class': 'post-form-input font-nunito-regular-normal', 'placeholder': 'Логин'})
        self.fields['username'].label = False
        self.fields['password'].widget = PasswordInput(attrs={'class': 'post-form-input font-nunito-regular-normal', 'placeholder':'Пароль'}) 
        self.fields['password'].label = False


class RegisterPostForm(ModelForm):
    """
    Форма для регистрации пользователей с формы сайта
    Внутри класса происходит переопределение метода сохранения пароля для того чтобы
    избавить от ошибки 'Неизвестный формат пароля или алгоритм хеширования'
    """
    # указываем с какой моделью будем работтать и какисми полями модели
    class Meta:
        model = User
        fields = ['username', 'password']

    # задаем класс формы и атрибут placeholder
    def __init__(self, *args, **kwargs):
        super(RegisterPostForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = TextInput(attrs={'class': 'post-form-input font-nunito-regular-normal', 'placeholder': 'Логин'})
        self.fields['username'].label = False
        self.fields['password'].widget = PasswordInput(attrs={'class': 'post-form-input font-nunito-regular-normal', 'placeholder':'Пароль'}) 
        self.fields['password'].label = False
 
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UpdateUserForm(ModelForm):
    # указываем с какой моделью будем работтать и какисми полями модели
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    # задаем класс формы и атрибут placeholder
    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget = TextInput(attrs={'class': 'post-form-input font-nunito-regular-normal', 'placeholder': 'Имя'})
        self.fields['first_name'].label = False
        self.fields['last_name'].widget = TextInput(attrs={'class': 'post-form-input font-nunito-regular-normal', 'placeholder':'Фамилия'}) 
        self.fields['last_name'].label = False
        self.fields['email'].widget = TextInput(attrs={'class': 'post-form-input font-nunito-regular-normal', 'placeholder':'email'}) 
        self.fields['email'].label = False


class ProfileUpdateForm(ModelForm):
    # указываем с какой моделью будем работтать и какисми полями модели
    class Meta:
        model = Profile
        fields = ['bio', 'photo']

    # задаем класс формы и атрибут placeholder
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['bio'].widget = Textarea(attrs={'class': 'post-form-input-textarea font-nunito-regular-normal', 'placeholder': 'Обо мне'})
        self.fields['bio'].label = False
        self.fields['photo'].widget = FileInput(attrs={'class': 'post-form-input font-nunito-regular-normal'})
        self.fields['photo'].label = False

class CommentCreateForm(ModelForm):
    # указываем с какой моделью будем работтать и какисми полями модели
    class Meta:
        model = Comment
        fields = ['content']

    # задаем класс формы и атрибут placeholder
    def __init__(self, *args, **kwargs):
        super(CommentCreateForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget = Textarea(attrs={'class': 'post-form-input-textarea font-nunito-regular-normal', 'placeholder': 'Комментарий'})
        self.fields['content'].label = False

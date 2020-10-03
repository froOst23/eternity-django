from .models import Post, Profile
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea, PasswordInput, FileInput
from django.contrib.auth.forms import AuthenticationForm, User

class NewPostForm(ModelForm):
    ALLOWED_TYPES = ['jpg', 'jpeg', 'png', 'gif']
    class Meta:
        model = Post
        fields = ['title', 'tag', 'content', 'image']
        widgets = {
            'title': TextInput(attrs={
                'class': 'post_form_input',
                'placeholder': 'Название поста'
            }),
            'tag': TextInput(attrs={
                'class': 'post_form_input',
                'placeholder': 'Используемые теги'
            }),
            'content': Textarea(attrs={
                'class': 'post_form_input_textarea',
                'placeholder': 'Описание поста'
            }),
            'image': FileInput(attrs={
                'class': 'post_form_input',
                'placeholder': 'Фото поста'
            })
        }


class LoginPostForm(AuthenticationForm, ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(LoginPostForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = TextInput(attrs={'class': 'post_form_input', 'placeholder': 'Логин'})
        self.fields['username'].label = False
        self.fields['password'].widget = PasswordInput(attrs={'class': 'post_form_input', 'placeholder':'Пароль'}) 
        self.fields['password'].label = False


class RegisterPostForm(ModelForm):
    """
    Форма для регистрации пользователей с формы сайта
    Внутри класса происходит переопределение метода сохранения пароля для того чтобы
    избавить от ошибки 'Неизвестный формат пароля или алгоритм хеширования'
    """
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': TextInput(attrs={
                'class': 'post_form_input',
                'placeholder': 'Логин'
            }),
            'password': PasswordInput(attrs={
                'class': 'post_form_input',
                'placeholder': 'Пароль'
            })
        }
 
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UpdateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': TextInput(attrs={
                'class': 'post_form_input',
                'placeholder': 'Имя'
            }),
            'last_name': TextInput(attrs={
                'class': 'post_form_input',
                'placeholder': 'Фамилия'
            }),
            'email': TextInput(attrs={
                'class': 'post_form_input',
                'placeholder': 'email'
            })
        }


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'photo']
        widgets = {
            'bio': Textarea(attrs={
                'class': 'post_form_input_textarea',
                'placeholder': 'Краткое описание'
            }),
            'photo': FileInput(attrs={
                'class': 'post_form_input'
            })
        }

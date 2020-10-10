from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('tag/<str:pk>', views.tag, name='tag'),
    path('accounts/profile/id<int:pk>/edit', views.update_profile, name='update-profile'),
    path('add-post', views.PostAddView.as_view(), name='add-post'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='detail'),
    path('post/<int:pk>/update', views.PostUpdateView.as_view(), name='update'),
    path('post/<int:pk>/delete', views.PostDeleteView.as_view(), name='delete'),
    path('accounts/login/', views.LoginPostView.as_view(), name='login'),
    path('accounts/logout', views.LogoutPostView.as_view(), name='logout'),
    path('registration', views.RegisterPostView.as_view(), name='registration'),
    path('accounts/profile/id<int:pk>', views.UserDetailView.as_view(), name='profile'),
    path('post/<int:pk>/add-comment', views.add_comment, name='add-comment'),
    path('update-comment/<int:pk>', views.CommentUpdateView.as_view(), name='update-comment')
    # path('accounts/profile/id<int:pk>/main', views.UpdateUserView.as_view(), name='main-edit'),
    # path('accounts/profile/id<int:pk>/extra', views.ProfileUpdateView.as_view(), name='extra-edit')
]

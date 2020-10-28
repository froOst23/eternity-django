from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('tag/<str:pk>', views.tag, name='tag'),
    path('accounts/profile/id<int:pk>/edit', views.update_profile, name='update_profile'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='detail'),
    path('post/new', views.PostAddView.as_view(), name='add_post'),
    path('post/<int:pk>/update', views.PostUpdateView.as_view(), name='update_post'),
    path('post/<int:pk>/delete', views.PostDeleteView.as_view(), name='delete_post'),
    path('accounts/login/', views.LoginPostView.as_view(), name='login'),
    path('accounts/logout', views.LogoutPostView.as_view(), name='logout'),
    path('registration', views.RegisterPostView.as_view(), name='registration'),
    path('accounts/profile/id<int:pk>', views.UserDetailView.as_view(), name='profile'),
    path('post/<int:pk>/comment/add', views.add_comment, name='add_comment'),
    path('post/<int:pk>/comment/reply<int:parent_id>', views.reply_comment, name='reply_comment'),
    path('comment/<int:pk>/update', views.CommentUpdateView.as_view(), name='update_comment'),
    path('comment/<int:pk>/delete', views.DeleteCommentView.as_view(), name='delete_comment')
]

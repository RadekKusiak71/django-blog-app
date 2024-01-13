from django.urls import path
from .views import HomeTemplateView, UserCreateView, UserPostListView, UserLoginView, PostCreateView, PostUpadteView, PostDetailView, PostDeleteView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home-page'),

    # post urls
    path('post/<int:pk>/', PostDetailView.as_view(), name='post'),
    path('posts/', UserPostListView.as_view(), name='post-user'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('post/edit/<int:pk>/', PostUpadteView.as_view(), name='post-edit'),
    path('post/create/', PostCreateView.as_view(), name='post-create'),

    # auth urls
    path('register/', UserCreateView.as_view(), name='register-page'),
    path('login/', UserLoginView.as_view(), name='login-page'),
    path('logout/', auth_views.LogoutView.as_view(
         next_page=reverse_lazy('login-page')), name='logout'),
]

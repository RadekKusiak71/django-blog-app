from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import Post, Profile
from .forms import RegisterForm, PostUpdateForm, PostCreateForm


class UserPostListView(ListView):
    template_name = 'home.html'

    def get_queryset(self) -> QuerySet:
        query = self.request.GET.get('q', '')
        queryset = Post.objects.filter(profile__user=self.request.user)
        if query:
            queryset = queryset.filter(
                profile__user=self.request.user, title__icontains=query)

        return queryset


class PostCreateView(CreateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostCreateForm
    success_url = reverse_lazy("home-page")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.profile = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)


class PostUpadteView(UpdateView):
    model = Post
    template_name = 'post_edit.html'
    form_class = PostUpdateForm

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset()


class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy("home-page")


class HomeTemplateView(ListView):
    template_name = 'home.html'

    def get_queryset(self) -> QuerySet:
        query = self.request.GET.get('q', '')
        queryset = Post.objects.all()
        if query:
            queryset = queryset.filter(title__icontains=query)

        return queryset


class UserCreateView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login-page')


class UserLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('home-page')

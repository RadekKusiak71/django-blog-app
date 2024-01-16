from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import Post, Profile, Comment
from .forms import RegisterForm, PostUpdateForm, PostCreateForm, CommentCreateForm
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin


class UserPostListView(LoginRequiredMixin, ListView):
    template_name = 'home.html'

    def get_queryset(self) -> QuerySet:
        query = self.request.GET.get('q', '')
        queryset = Post.objects.filter(profile__user=self.request.user)
        if query:
            queryset = queryset.filter(
                profile__user=self.request.user, title__icontains=query)

        return queryset


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostCreateForm
    success_url = reverse_lazy("home-page")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.profile = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)


class PostUpadteView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'post_edit.html'
    form_class = PostUpdateForm

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset()


class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'post.html'
    form_class = CommentCreateForm

    def get_success_url(self):
        return reverse('post', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.profile = Profile.objects.get(user=self.request.user)
        comment.post = self.object
        comment.save()

        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(
            post=context['post']).order_by('-created_date')
        return context


class PostDeleteView(LoginRequiredMixin, DeleteView):
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

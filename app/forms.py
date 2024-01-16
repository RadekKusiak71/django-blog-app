from typing import Any
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment
from ckeditor.fields import CKEditorWidget


class CommentCreateForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('body',)


class PostCreateForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = ['title', 'description', 'body', 'post_image']


class PostUpdateForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = ['title', 'description', 'body', 'post_image']


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    firstname = forms.CharField(max_length=255, required=True)
    lastname = forms.CharField(max_length=255, required=True)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'label': 'Email'
        })
        self.fields['firstname'].widget.attrs.update({
            'label': 'Firstname'
        })
        self.fields['lastname'].widget.attrs.update({
            'label': 'Lastname'
        })

    class Meta:
        model = User
        fields = ('username', 'firstname', 'lastname',
                  'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('firstname')
        user.last_name = self.cleaned_data.get('lastname')

        if commit:
            user.save()
        return user

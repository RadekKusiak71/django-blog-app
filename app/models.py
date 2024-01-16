from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


def get_upload_location(instance, file_name):
    return 'profiles/%s/%s' % (instance.user.username, file_name)


def get_upload_location_post(instance, file_name):
    return 'posts/%s/%s' % (instance.profile.user.username, file_name)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to=get_upload_location, validators=[FileExtensionValidator(['png', 'jpeg', 'jpg'])], null=True, blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    description = models.TextField(max_length=255)
    post_image = models.ImageField(upload_to=get_upload_location_post, validators=[
                                   FileExtensionValidator(['png', 'jpeg', 'jpg'])], null=True, blank=True)
    title = models.CharField(max_length=255)
    body = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Post created by %s at %s" % (self.profile.user.username, self.created_date)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Comment created by %s at %s' % (self.profile.user.username, self.created_date)

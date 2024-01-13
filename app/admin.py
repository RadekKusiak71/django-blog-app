from django.contrib import admin
from .models import Post, Profile, Comment, Rate


admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Rate)
# Register your models here.

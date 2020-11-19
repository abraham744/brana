from django.contrib import admin
from .models import Post, Comment, Category, Notification, Message


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(Notification)
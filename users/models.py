from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.conf import settings

from blog.models import Post


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    cover_image = models.FileField(default='channel-banner.png', upload_to='profile_pics')
    location = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=80, null=True, blank=True)
    last_name = models.CharField(max_length=80, null=True, blank=True)
    url = models.CharField(max_length=80, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    bio = models.TextField(max_length=300,default='be the change u want to see in the world')
    about = models.TextField(max_length=500,default='welcome to branagram!')
    favorites = models.ManyToManyField(Post)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        SIZE = 250, 250

        if self.image:
            pic = Image.open(self.image.path)
            pic.thumbnail(SIZE, Image.LANCZOS)
            pic.save(self.image.path)

        if self.cover_image:

            c_img = Image.open(self.cover_image.path)

            c_img.save(self.cover_image.path)

class Friend(models.Model):
    following = models.ManyToManyField(User)
    follower = models.ManyToManyField(User,related_name='follow')
    current_user = models.ForeignKey(User,related_name='owner', null=True,on_delete=models.CASCADE)
    blacklists = models.ManyToManyField(User, related_name='blocked_users')
    blacklisters = models.ManyToManyField(User, related_name='blocker_users')

    @classmethod
    def follow(cls,current_user,new_user):
        follow, created = cls.objects.get_or_create(current_user=current_user)
        follow.following.add(new_user)

        follow, created = cls.objects.get_or_create(current_user=new_user)
        follow.follower.add(current_user)

    @classmethod
    def unfollow(cls, current_user, new_user):
        follow, created = cls.objects.get_or_create(current_user=current_user)
        follow.following.remove(new_user)


    @classmethod
    def block(cls, current_user, new_user):
        block, created = cls.objects.get_or_create(current_user=current_user)
        block.blacklists.add(new_user)
        block.following.remove(new_user)

        block, created = cls.objects.get_or_create(current_user=new_user)
        block.blacklisters.add(current_user)
        block.follower.remove(current_user)

    @classmethod
    def unblock(cls, current_user, new_user):
        block, created = cls.objects.get_or_create(current_user=current_user)
        block.blacklists.remove(new_user)

        block, created = cls.objects.get_or_create(current_user=new_user)
        block.blacklisters.remove(new_user)

    def __str__(self):
        return f'{self.current_user.username} Relationships'




















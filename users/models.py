from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.conf import settings

from blog.models import Post


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    cover_image = models.FileField(default='banner.jpg', upload_to='profile_pics')
    bio = models.TextField(max_length=300,default='be the change u want to see in the world')
    about = models.TextField(max_length=500,default='welcome to branagram!')
    favorites = models.ManyToManyField(Post)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
        c_img = Image.open(self.cover_image.path)
        if c_img.height > 380 and c_img.width < 1500:
            final_size = (380, 1500)
            c_img.thumbnail(final_size)
            c_img.save(self.cover_image.path)

class Friend(models.Model):
    following = models.ManyToManyField(User)
    follower = models.ManyToManyField(User,related_name='follow')
    current_user = models.ForeignKey(User,related_name='owner', null=True,on_delete=models.CASCADE)


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

    def __str__(self):
        return f'{self.current_user.username} Relationships'




















import textwrap
import uuid
from ckeditor.fields import RichTextField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Max
from django.urls import reverse
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100,default= 'My Brana')
    slug = models.SlugField(unique=True, default=uuid.uuid1)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='cover_folder/', blank=True, null=True, verbose_name='upload your files')

    def __str__(self):
        return self.name
    def total_album(self):
        return self.name.count()

    def get_absolute_url(self):
        return reverse('upload')


class Notification(models.Model):
    NOTIFICATION_TYPES = ((1, 'Like'), (2, 'Comment'), (3, 'Follow'), (4, 'Reply'))
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name="noti_post", blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_from_user")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_to_user")
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    text_preview = models.CharField(max_length=90, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)


class Tag(models.Model):
    title = models.CharField(max_length=75, verbose_name='Tag')
    slug = models.SlugField(null=False, unique=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def get_absolute_url(self):
        return reverse('tags', args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField(max_length=200)
    meme_top = models.CharField(max_length=100)
    meme_bottom = models.CharField(max_length=100)
    content = RichTextField()
    tags = models.ManyToManyField(Tag, related_name='tags')
    photo = models.ImageField(upload_to='pic_folder/', blank=True, null=True,
                              verbose_name='Click to upload image files')
    video = models.FileField(upload_to='dox_folder/', blank=True, null=True, verbose_name='Click to upload video files')
    thumbnail = models.ImageField(upload_to='pic_folder/', blank=True, null=True,
                                  verbose_name='Click to upload  thumbnail cover...')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, max_length=255, default='1')
    likes = models.ManyToManyField(User, related_name='blog_posts')
    dislikes = models.ManyToManyField(User, related_name='dislikes')
    hises = models.ManyToManyField(User, related_name='comment_count')
    viewers = models.ManyToManyField(User, related_name='viewers')
    no_viewers = models.PositiveIntegerField(null=True)
    is_seen = models.BooleanField(default=False)

    def total_likes(self):
        return self.likes.count()

    def total_views(self):
        no_viewers = self.viewers.count()
        return no_viewers

    def total_comments(self):
        return self.hises.count()

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        if self.meme_bottom:
            im = Image.open(self.photo.path)
            draw = ImageDraw.Draw(im)
            image_width, image_height = im.size

            # load font
            font_path = './fonts/impact/impact.ttf'
            font_size = 7
            font = ImageFont.truetype(font=font_path, size=int(image_height * font_size) // 100)

            top_text = self.meme_top
            bottom_text = self.meme_bottom
            top_text = top_text.upper()
            bottom_text = bottom_text.upper()

            # text wrapping
            char_width, char_height = font.getsize('A')
            chars_per_line = image_width // char_width
            top_lines = textwrap.wrap(top_text, width=chars_per_line)
            bottom_lines = textwrap.wrap(bottom_text, width=chars_per_line)

            # draw top lines
            y = 10
            a = 1
            for line in top_lines:
                line_width, line_height = font.getsize(line)
                x = (image_width - line_width) / 2
                draw.text((x - a, y), line, font=font, fill='black')
                draw.text((x, y - a), line, font=font, fill='black')
                draw.text((x + a, y), line, font=font, fill='black')
                draw.text((x, y + a), line, font=font, fill='black')

                draw.text((x, y), line, fill='white', font=font)
                y += line_height

                # draw bottom lines
                y = image_height - char_height * len(bottom_lines) - 15
            for line in bottom_lines:
                line_width, line_height = font.getsize(line)
                x = (image_width - line_width) / 2
                draw.text((x - a, y), line, font=font, fill='black')
                draw.text((x, y - a), line, font=font, fill='black')
                draw.text((x + a, y), line, font=font, fill='black')
                draw.text((x, y + a), line, font=font, fill='black')

                draw.text((x, y), line, fill='white', font=font)
                y += line_height
            im.save(self.photo.path)


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = RichTextField()
    likes = models.ManyToManyField(User, related_name='comment_posts')
    dislikes = models.ManyToManyField(User, related_name='dislikes_posts')
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    parent = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    body = RichTextField(max_length=1000, blank=True, null=True)
    photo = models.FileField(upload_to='message_folder/', blank=True, null=True, verbose_name='upload your files')
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def send_message(from_user,to_user, body,file):
        sender_message = Message(
            user=from_user,
            sender=from_user,
            recipient=to_user,
            body=body,
            photo= file,
            is_read=True)
        sender_message.save()

        if from_user != to_user:
            recipient_message = Message(
                user=to_user,
                sender=from_user,
                body=body,
                photo= file,
                recipient=from_user, )
            recipient_message.save()
        return sender_message

    def get_messages(user):
        messages = Message.objects.filter(user=user).values('recipient').annotate(last=Max('date')).order_by('-last')
        users = []
        for message in messages:
            users.append({
                'user': User.objects.get(pk=message['recipient']),
                'last': message['last'],
                'latest': Message.objects.filter(user=user, recipient__pk = message['recipient']),
                'unread': Message.objects.filter(user=user, recipient__pk=message['recipient'], is_read=False).count()
            })
        return users

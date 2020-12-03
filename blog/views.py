from datetime import timezone

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.template import loader
from django.views.generic.edit import FormMixin

from blog.models import Message, Category, Tag
from django.db.models import Q
from blog.models import Notification

from users.models import Friend, Profile
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from blog.form import CommentForm, PhotoForm, VideoForm, MemeForm, UpdateForm, ReplyForm, AlbumUpdateForm
from .models import Post, Comment


def home(request):
    context = {
        'posts': Post.objects.all(),
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get(self, request):
        if request.user.is_authenticated:
            users = None
            blacklists = None
            blacklisters = None
            follower = None
            ffollower = None
            blogs = None
            query = request.GET.get("q")
            if query:
                users = User.objects.filter(Q(username__icontains=query))
                for user in users:
                    follow = Friend.objects.filter(current_user=user).first()
                    if follow:
                        follower = Friend.objects.filter(current_user=user).get(current_user=user).follower.all()
                    # followings = Friend.objects.filter(current_user=user).first().following.all()

                blogs = Post.objects.filter(Q(title__icontains=query))
            notifications = Notification.objects.filter(user=request.user).order_by('-date')
            count_notifications = Notification.objects.filter(user=request.user, is_seen=False).count()
            directs_count = Message.objects.filter(user=request.user, is_read=False).count()

            friend = Friend.objects.filter(current_user=request.user).first()
            if friend:
                blacklists = Friend.objects.filter(current_user=request.user).first().blacklists.all()
                blacklisters = Friend.objects.filter(current_user=request.user).first().blacklisters.all()
                friends = friend.following.all()
                friend = friend.follower.all()
            else:
                friends = User.objects.none()
            # friends = friend.users.all()
            myalbums = Category.objects.filter(author=request.user)
            posts = Post.objects.all().filter(Q(author_id__in=friends) | Q(author=request.user)).order_by('?')
            myposts = Post.objects.filter(author=request.user).order_by('-date_posted')
            args = {'posts': posts, 'myalbums': myalbums, 'myposts': myposts, 'users': users, 'friend': friend,
                    'friends': friends, 'blacklists': blacklists, 'blacklisters': blacklisters, 'blogs': blogs,
                    'directs_count': directs_count, 'ffollower': ffollower, 'follower': follower,
                    'count_notifications': count_notifications, 'notifications': notifications}
            return render(request, self.template_name, args)
        else:
            users = None
            posts = Post.objects.all().order_by('no_viewers')
            query = request.GET.get("q")
            if query:
                users = User.objects.filter(Q(username__icontains=query))
            args = {'posts': posts, 'users': users}
            return render(request, self.template_name, args)


class WatchVideoView(ListView):
    model = Post
    template_name = 'blog/home2.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get(self, request):
        if request.user.is_authenticated:
            users = None
            blacklists = None
            blacklisters = None
            follower = None
            ffollower = None
            blogs = None
            query = request.GET.get("q")
            if query:
                users = User.objects.filter(Q(username__icontains=query))
                for user in users:
                    follow = Friend.objects.filter(current_user=user).first()
                    if follow:
                        follower = Friend.objects.filter(current_user=user).get(current_user=user).follower.all()
                    # followings = Friend.objects.filter(current_user=user).first().following.all()

                blogs = Post.objects.filter(Q(title__icontains=query))
            notifications = Notification.objects.filter(user=request.user).order_by('-date')
            count_notifications = Notification.objects.filter(user=request.user, is_seen=False).count()
            directs_count = Message.objects.filter(user=request.user, is_read=False).count()

            friend = Friend.objects.filter(current_user=request.user).first()
            if friend:
                blacklists = Friend.objects.filter(current_user=request.user).first().blacklists.all()
                blacklisters = Friend.objects.filter(current_user=request.user).first().blacklisters.all()
                friends = friend.following.all()
                friend = friend.follower.all()
            else:
                friends = User.objects.none()
            # friends = friend.users.all()
            myalbums = Category.objects.filter(author=request.user)
            posts = Post.objects.all().filter(Q(author_id__in=friends) | Q(author=request.user)).order_by('?')
            myposts = Post.objects.filter(author=request.user).order_by('-date_posted')
            args = {'posts': posts, 'myalbums': myalbums, 'myposts': myposts, 'users': users, 'friend': friend,
                    'friends': friends, 'blacklists': blacklists, 'blacklisters': blacklisters, 'blogs': blogs,
                    'directs_count': directs_count, 'ffollower': ffollower, 'follower': follower,
                    'count_notifications': count_notifications, 'notifications': notifications}
            return render(request, self.template_name, args)
        else:
            users = None
            posts = Post.objects.all().order_by('no_viewers')
            query = request.GET.get("q")
            if query:
                users = User.objects.filter(Q(username__icontains=query))
            args = {'posts': posts, 'users': users}
            return render(request, self.template_name, args)


class PlaylistView(ListView):
    model = Category
    template_name = 'blog/playlist.html'
    context_object_name = 'playlists'

    def get_queryset(self):
        users = get_object_or_404(User, username=self.kwargs.get('username'))
        return Category.objects.filter(author=users)


class CategoryView(ListView):
    model = Category
    template_name = 'blog/album.html'
    context_object_name = 'albums'

    def get_queryset(self):
        users = get_object_or_404(User, username=self.kwargs.get('username'))
        return Category.objects.filter(author=users)


class Favorited_View(ListView):
    model = Post
    template_name = 'blog/favorited_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        profile = Profile.objects.get(user=user)
        return profile.favorites.all().order_by('-date_posted')


class CategoryPostView(ListView):
    model = Post
    template_name = 'blog/category_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        name = get_object_or_404(Category, name=self.kwargs.get('name'))
        return Post.objects.filter(category=name).order_by('-date_posted')


class CategoryVideoView(ListView):
    model = Post
    template_name = 'blog/category_videos.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        name = get_object_or_404(Category, name=self.kwargs.get('name'))
        return Post.objects.filter(category=name).order_by('-date_posted')


class PostDetailView(FormMixin, DetailView):
    model = Post
    form_class = CommentForm

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        Post.objects.filter(viewers=self.request.user, is_seen=False).update(is_seen=True)
        viewscount(self.request.user, stuff)
        favorited = False

        if self.request.user.is_authenticated:
            profile = Profile.objects.get(user=self.request.user)
            if profile.favorites.filter(id=self.kwargs['pk']).exists():
                favorited = True

        notifications = Notification.objects.filter(user=self.request.user).order_by('-date')
        count_notifications = Notification.objects.filter(user=self.request.user, is_seen=False).count()
        total_comments = stuff.total_comments()
        total_likes = stuff.total_likes()
        total_views = stuff.total_views()
        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        posts = Post.objects.filter(author=stuff.author).exclude(id=self.kwargs['pk']).order_by('-date_posted')
        context['user'] = self.request.user
        context['comments'] = Comment.objects.filter(post=self.object)
        context['form'] = self.get_form()
        context["total_likes"] = total_likes
        context["total_views"] = total_views
        context["total_comments"] = total_comments
        context["liked"] = liked
        context["favorited"] = favorited
        context["notifications"] = notifications
        context["count_notifications"] = count_notifications
        context["posts"] = posts
        return context

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        users = self.request.user
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = users
                comment.save()
                post.hises.add(comment.author)
                notify = Notification(post=post, text_preview=comment.text, sender=comment.author, user=post.author,
                                      notification_type=2)
                notify.save()
                return redirect('post_detail', pk=self.kwargs['pk'])
        else:
            form = CommentForm()
            return redirect('post_detail', pk=self.kwargs['pk'])

    def form_valid(self, form):
        form.instance.post = self.object
        form.save()
        return super().form_valid(form)


@login_required
def favorite(request, pk):
    user = request.user
    post = get_object_or_404(Post, id=pk)
    profile = Profile.objects.get(user=user)
    if profile.favorites.filter(id=pk).exists():
        profile.favorites.remove(post)
    else:
        profile.favorites.add(post)
    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))


def viewscount(viewer, post):
    post.viewers.add(viewer)
    return None


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))

    like = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        notify = Notification.objects.filter(post=post, sender=request.user, user=post.author, notification_type=1)
        notify.delete()
        like = False
    else:
        post.likes.add(request.user)
        notify = Notification(post=post, sender=request.user, user=post.author, notification_type=1)
        notify.save()
        like = True

    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))


def tags(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag).order_by('-posted')

    context = {
        'posts': posts,
        'tag': tag,
    }
    return HttpResponse(request, 'blog/tags.html', context)


def dislikecomment(request, pk):
    comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
    dislike = False
    if comment.dislikes.filter(id=request.user.id).exists():
        comment.dislikes.remove(request.user)
        notify = Notification.objects.filter(post=comment.post, sender=request.user, user=comment.author,
                                             notification_type=5)
        notify.delete()
        dislike = False
    else:
        comment.likes.remove(request.user)
        comment.dislikes.add(request.user)
        # notification
        dislike = True
    return HttpResponseRedirect(reverse('post_detail', args=[str(comment.post.pk)]))


def Likecomment(request, pk):
    comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
    like = False
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
        notify = Notification.objects.filter(post=comment.post, sender=request.user, user=comment.author,
                                             notification_type=5)
        notify.delete()
        like = False
    else:
        comment.likes.add(request.user)
        comment.dislikes.remove(request.user)
        # notification
        like = True
    return HttpResponseRedirect(reverse('post_detail', args=[str(comment.post.pk)]))


class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name', 'photo', ]

    def get_form(self, form_class=None):
        form = super(AlbumCreateView, self).get_form(form_class)
        return form

    def get_initial(self):
        return {
            'author': self.request.user,
        }

    def form_valid(self, form):
        form.instance.author = self.request.user
        album = form.save(commit=False)
        album.save()
        return super().form_valid(form)


class VideoCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = VideoForm

    def get_form_kwargs(self):
        kwargs = super(VideoCreateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save(commit=False)
        post.save()
        return super().form_valid(form)


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PhotoForm

    def get_form_kwargs(self):
        kwargs = super(PhotoCreateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save(commit=False)
        post.save()
        return super().form_valid(form)


class MemeCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = MemeForm

    def get_form_kwargs(self):
        kwargs = super(MemeCreateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save(commit=False)
        post.save()
        return super().form_valid(form)


@login_required()
def uploadWhat(request):
    return render(request, 'blog/upload.html', {'title': 'choose post items'})

@login_required
def relations(request, pk):
    blacklists = None
    blacklisters = None
    if pk:
        friend = Friend.objects.filter(current_user=request.user).first()
        if friend:
            friends = friend.following.all()
            blacklists = friend.blacklists.all()
            blacklisters = friend.blacklisters.all()
            friend = friend.follower.all()
        else:
            friends = User.objects.none()
        users = User.objects.get(pk=pk)
        followers = None
        followings = None
        follow = Friend.objects.filter(current_user=users).first()
        if follow:
            followings = follow.following.all()
            followers = follow.follower.all()
        else:
            friends = User.objects.none()

    args = {'users': users, 'follower': followers, 'blacklists': blacklists, 'blacklisters': blacklisters, 'friend': friend,
            'friends': friends, 'followings': followings}
    return render(request, 'blog/relationships.html', args)

@login_required
def profile(request, pk):
    blacklists = None
    blacklisters = None
    if pk:
        friend = Friend.objects.filter(current_user=request.user).first()
        if friend:
            friends = friend.following.all()
            blacklists = friend.blacklists.all()
            blacklisters = friend.blacklisters.all()
            friend = friend.follower.all()
        else:
            friends = User.objects.none()
        users = User.objects.get(pk=pk)
        total_album = Category.objects.filter(author=users).count()
        total_post = Post.objects.filter(author=users,).count()
        followers = None
        followings = None
        follow = Friend.objects.filter(current_user=users).first()
        if follow:
            followings = follow.following.all()
            followers = follow.follower.all()
        else:
            friends = User.objects.none()

    args = {'users': users, 'follower': followers, 'total_photo': total_post, 'total_video': total_post,
            'total_album': total_album, 'blacklists': blacklists, 'blacklisters': blacklisters, 'friend': friend,
            'friends': friends, 'followings': followings}
    return render(request, 'blog/profile.html', args)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = UpdateForm

    def get_form_kwargs(self):
        kwargs = super(PostUpdateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save(commit=False)
        post.save()
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    fields = AlbumUpdateForm

    def get_form_kwargs(self):
        kwargs = super(CategoryUpdateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save(commit=False)
        post.save()
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


@login_required
def add_reply_to_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    posts = Post.objects.filter(author=post.author).exclude(id=post.id).order_by('-date_posted')
    comments = Comment.objects.filter(post=post)
    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent = comment
            reply.post = post
            reply.save()
            notify = Notification(post=post, sender=reply.author, user=comment.author, notification_type=4)
            notify.save()
            notify = Notification(post=post, sender=reply.author, user=post.author, notification_type=2)
            notify.save()
            return redirect('add_reply', pk=comment.pk)
    else:
        form = ReplyForm()
    context = {
        'comment': comment, 'posts': posts, 'comments': comments, 'form': form}
    return render(request, 'blog/add_reply.html', context)


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    comment.delete()
    post.hises.remove(comment.author)
    post = comment.post
    notify = Notification.objects.filter(post=post, sender=request.user, user=post.author, notification_type=2)
    notify.delete()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def ShowNOtifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-date')
    Notification.objects.filter(user=user, is_seen=False).update(is_seen=True)
    myposts = Post.objects.filter(author=request.user).order_by('-date_posted')
    context = {
        'notifications': notifications, 'myposts': myposts
    }
    return render(request, 'blog/notifications.html', context)


@login_required
def DeleteNotification(request, noti_id):
    user = request.user
    Notification.objects.filter(id=noti_id, user=user).delete()
    return redirect('show-notifications')


@login_required
def CountNotifications(request):
    count_notifications = 0
    if request.user.is_authenticated:
        count_notifications = Notification.objects.filter(user=request.user, is_seen=False).count()

    return {'count_notifications': count_notifications}


@login_required
def Inbox(request):
    messages = Message.get_messages(user=request.user)
    active_direct = None
    active_pic = None
    active_user = None
    directs = None

    if messages:
        message = messages[0]
        active_direct = message['user'].username
        active_user = User.objects.get(username=active_direct)
        active_pic = message['user'].profile.image
        directs = Message.objects.filter(user=request.user, recipient=message['user'])
        directs.update(is_read=True)
        for message in messages:
            if message['user'].username == active_direct:
                message['unread'] = 0
    context = {
        'directs': directs,
        'messages': messages,
        'active_pic': active_pic,
        'active_direct': active_direct, 'active_user': active_user,
    }
    return render(request, 'blog/direct.html', context)


@login_required
def UserSearch(request):
    query = request.GET.get("q")
    context = {}

    if query:
        users = User.objects.filter(Q(username__icontains=query))

        # Pagination
        paginator = Paginator(users, 6)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)

        context = {
            'users': users_paginator,

        }
    return render(request, 'blog/search_user.html', context)


@login_required
def Directs(request, username):
    user = request.user
    active_pic = None
    active_user = None
    users = None

    messages = Message.get_messages(user=user)
    active_direct = username
    active_user = User.objects.get(username=active_direct)
    directs = Message.objects.filter(user=user, recipient__username=username)
    directs.update(is_read=True)
    if messages:
        message = messages[0]
        active_pic = message['user'].profile.image

    for message in messages:
        if message['user'].username == username:
            message['unread'] = 0

    context = {
        'active_user': active_user,
        'active_pic': active_pic,
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
    }
    return render(request, 'blog/direct.html', context)


@login_required
def DeleteMessage(request, username=None):
    Message.get_messages(user=request.user).delete()
    return redirect('inbox')


@login_required
def NewConversation(request, username):
    from_user = request.user
    body = 'you are joined succesfullyl'
    try:
        to_user = User.objects.get(username=username)
    except Exception as e:
        return redirect('usersearch')
    if from_user != to_user:
        #     Message.send_message(from_user, to_user, body)
        return redirect('directs', to_user)


@login_required
def SendDirect(request):
    from_user = request.user
    if request.method == 'POST':
        to_user_username = request.POST.get('to_user')
        body = request.POST.get('body')
        to_user = User.objects.get(username=to_user_username)
        Message.send_message(from_user, to_user, body, file=None)
        return redirect('inbox')
    else:
        HttpResponseBadRequest()



def checkDirects(request):
    directs_count = 0
    if request.user.is_authenticated:
        directs_count = Message.objects.filter(user=request.user, is_read=False).count()

    return {'directs_count': directs_count}

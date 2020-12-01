from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import ListView

from blog.models import Post, Notification, Category
from .models import Friend, Profile
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request, username=None):
    if request.method == 'POST':
        users= request.user.pk
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile_me',users)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)


def view_profile(request, pk, username=None):
    if pk:
        users = User.objects.get(pk=pk)
        user_posts = Post.objects.filter(author=users)
    args = {'users': users, 'user_posts': user_posts}
    paginate_by = 5
    return render(request, 'users/user_profile.html', args)

@login_required
def blacklist(request, pk):
    if request.user.is_authenticated:
        to_block = User.objects.get(pk=pk)
        if Friend.objects.filter(blacklists=to_block).exists():
            Friend.unblock(request.user, to_block)
        else:
            Friend.block(request.user, to_block)
    return redirect('profile_me',to_block.pk)
@login_required
def change_friends(request, operation, pk):
    if request.user.is_authenticated:
        to_follow = User.objects.get(pk=pk)
        if operation == 'add':
            Friend.follow(request.user, to_follow)
            notify = Notification( sender=request.user, user=to_follow,notification_type=3)
            notify.save()
        elif operation == 'remove':
            Friend.unfollow(request.user, to_follow)
            notify = Notification.objects.filter( sender=request.user,user =to_follow, notification_type=3)
            notify.delete()
        return redirect('profile_me',to_follow.pk)

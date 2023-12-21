from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .forms import *
from .models import *
def index(request):
    return render(request, "network/index.html")
# ----------------------------------------------------------------------#
def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

# ---------------------------------------------------------------------------#
# creating new post
def index(request):
        likes = LikesModel.objects.all()
        postLikes = []
        try:
            for like in likes:
                if like.user.id == request.user.id:
                    postLikes.append(like.post.id)
        except:
            postLikes = [] 

#-----------------------------------------------------------#
        PostFeed = New_Post.objects.all().order_by('id')
        Navigation = Paginator(PostFeed, 5)
        pageNum = request.GET.get('page')
        post_page = Navigation.get_page(pageNum)
        form = NewPostForm(request.POST or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            form = NewPostForm()
            return redirect('index')
        return render(request, "network/index.html",{
                    'form': form, 
                    'PostFeed': PostFeed, 
                    "post_page": post_page,
                    "postLikes":postLikes,
                        })
# ---------------------------------------------------------------------------#
# showing user profile
def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    PostFeed = New_Post.objects.filter(user=user).order_by('id').reverse()

    # followers fun
    followers = followers_dashboard.objects.filter(follower=user)
    following = followers_dashboard.objects.filter(user=user)

    # check following
    try:
        check = followers.filter(user=User.objects.get(pk=request.user.id))
        if len(check) != 0:
            already_following = True
        else:
            already_following = False
    except:
        already_following = False

    Navigation = Paginator(PostFeed, 7)
    pageNum = request.GET.get('page')
    post_page = Navigation.get_page(pageNum)

    form = NewPostForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        form = NewPostForm()
    context = {
        'form': form,
        'PostFeed': PostFeed,
        "post_page": post_page,
        "user_owner": user.username,
        "following": following,
        "followers": followers,
        "profile_owner": user,
        "already_following": already_following,
    }
    return render(request, "network/profile.html", context)
# ------------------------------------------------------------------------------#


def follow(request):
    btn_follow = request.POST['btn_follow']
    current_user = User.objects.get(pk=request.user.id)
    user_data = User.objects.get(username=btn_follow)
    done = followers_dashboard(user=current_user, follower=user_data)
    done.save()
    user_id = user_data.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))
# -------------------------------------------------------------------------


def unfollow(request):
    btn_follow = request.POST['btn_follow']
    current_user = User.objects.get(pk=request.user.id)
    user_data = User.objects.get(username=btn_follow)
    done = followers_dashboard.objects.get(
        user=current_user, follower=user_data)
    done.delete()
    user_id = user_data.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))
# -------------------------------------------------------------------------


def following(request):
    likes = LikesModel.objects.all()
    postLikes = []
    try:
        for like in likes:
            if like.user.id == request.user.id:
                postLikes.append(like.post.id)
    except:
            postLikes = [] 

    current_login_user = request.user.id
    followers = followers_dashboard.objects.filter(user=current_login_user)
    followers_post_feed = New_Post.objects.all().order_by('date')
    post_feed = []
    for display in followers_post_feed:
        for author in followers:
            if author.follower == display.user:
                post_feed.append(display)
    if len(followers) == 0:
        messages.warning(request, "You Are Not Following Anyone!")
    Navigation = Paginator(post_feed, 7)
    pageNum = request.GET.get('page')
    post_page = Navigation.get_page(pageNum)
    context = {
        "post_page": post_page,
        "postLikes":postLikes,
    }
    return render(request, "network/following.html", context)
# -------------------------------------------------------------------------
#fun for editing post
def EditPost(request, pk):
    Post = get_object_or_404(New_Post, id=pk)
    form = NewPostForm(request.POST or None, instance=Post)
    if request.user.username == Post.user.username:
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user
                obj.save()
                form = NewPostForm()
                messages.success(request, "your post has been updated successfully")
            return redirect('index')
    # return render(request, "network/EditPost.html", {'form': form, "Post": Post})
#-----------------------------------------------------------------------------------------
#fun for deleting post
def DeletePost(request, pk):
    Post = get_object_or_404(New_Post, id=pk)
    if request.user.username == Post.user.username:
        Post.delete()
        messages.success(request, "your post has been Deleted successfully ")
        return redirect('index')
#-----------------------------------------------------------------------------------------
def like (request,pk):
    post = New_Post.objects.get(id=pk)
    user = get_object_or_404(User,id=request.user.id)
    addLike = LikesModel(user=user,post=post)
    addLike.save()
    return redirect('index')

def unlike (request,pk):
    post = New_Post.objects.get(id=pk)
    user = get_object_or_404(User,id=request.user.id)
    addLike = LikesModel.objects.filter(user=user,post=post)
    addLike.delete()
    return redirect('index')




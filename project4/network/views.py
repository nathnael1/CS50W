from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError,transaction
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import User,Profile,Following,Followers,Publish,Like
import json

#user id request.user.id
def index(request):
    published = Publish.objects.all().order_by('-time')
    liked = Like.objects.filter(user=request.user).exists()
    if request.user.is_authenticated:
        if Profile.objects.filter(user=request.user).exists():
           request.session['profileSet'] = Profile.objects.get(user=request.user).profileSet
        else:
           return HttpResponseRedirect(reverse("profile"))
        if request.session['profileSet']:
            if liked:
                return render(request, "network/index.html",{
                    'published':published,
                    'button':True
                })
            else:
                return render(request, "network/index.html",{
                    'published':published,
                    'button':False
                })
        else:
            return HttpResponseRedirect(reverse("profile"))
    
    return render(request, "network/index.html",{
        'published':published
    })
def following(request):
    if request.user.is_authenticated:
        following = Following.objects.filter(user=request.user.id)
        followinglist = [follow.following.id for follow in following]
        published = Publish.objects.filter(user__in=followinglist).order_by('-time')
        return render(request, "network/following.html", {
            'published': published
        })
    return HttpResponseRedirect(reverse('index'))
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
def profile(request):
    if request.method == "POST":
        bio = request.POST["bio"]
        imagelink = request.POST["imagelink"]
        profile = Profile(user=request.user,bio=bio,image_link=imagelink,profileSet=True)
        profile.save()
        request.session['profileSet'] = profile.profileSet
        return HttpResponseRedirect(reverse("index"))
    return render(request, "network/profile.html")


def publish(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            content = request.POST["content"]
            publish = Publish(user=request.user,content=content)
            publish.save()
            return HttpResponseRedirect(reverse("index"))
        return HttpResponseRedirect(reverse("index"))
    return HttpResponseRedirect(reverse("login"))

@csrf_exempt
def profile_view(request,username):
    followerpersons = []
    user = User.objects.get(username=username)
    username = user.username
    profile = Profile.objects.get(user=user)
    bio = profile.bio
    image_link = profile.image_link
    followers = Followers.objects.filter(user=user).count()
    for follower in Followers.objects.filter(user = user):
        followerpersons.append(follower.follower.username)
    following = Following.objects.filter(user=user).count()

    if request.user.username.strip().lower() in (name.strip().lower() for name in followerpersons):
        followed = True
    else:
        followed = False
    postNumber = Publish.objects.filter(user = user).count()
    publishes = Publish.objects.filter(user = user).order_by('-time')
    return render(request, "network/profileview.html",{

        'followed':followed,
        'username':username,
        'bio':bio,
        'image_link':image_link,
        'profile':profile,
        'followers':followers,
        'following':following,
        'postNumber':postNumber,
        'publishes':publishes
    })
@csrf_exempt
def follow(request, username):
    if request.method == "PUT":
        with transaction.atomic():
            user = User.objects.get(username=username)
            checkfollow = Followers.objects.filter(user=user, follower=request.user).exists()
            checkfollowing = Following.objects.filter(user=request.user, following=user).exists()
            if checkfollow or checkfollowing:
                return JsonResponse({"message": "already followed"})
            follow = Followers(user=user, follower=request.user)
            following = Following(user=request.user, following=user)
            follow.save()
            following.save()
        return JsonResponse({"message": "followed successfully"})
    return HttpResponseRedirect(reverse("index"))

@csrf_exempt
def unfollow(request,username):
    if request.method == "PUT":
        user = User.objects.get(username=username)
        previousfollow = Followers.objects.filter(user=user,follower=request.user).first()
        previousfollowing = Following.objects.filter(user=request.user,following=user).first()
        previousfollow.delete()
        previousfollowing.delete()
        return JsonResponse({"message":"unfollowed succesfully"})
    return HttpResponseRedirect(reverse("index"))
@csrf_exempt
def edit(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        post_id = data["post_id"]
        content = data["content"]
        publish = Publish.objects.get(id=post_id)
        publish.content = content
        publish.save()
        return JsonResponse({"message":"edited successfully","content":content})
    return HttpResponseRedirect(reverse("index"))

def like(request):
    if request.method == "PUT":
        with transaction.atomic():
            data = json.loads(request.body)
            post_id = data["post_id"]
            likedPublish = Like.objects.filter(user=request.user,publishliked = post_id).exists()
            if likedPublish:
                liked = Like.objects.filter(user=request.user,publishliked = post_id).first()
                liked.delete()
                Publish.objects.get(id=post_id).likes-=1
                return JsonResponse({"message":"unliked","likedNumber":Publish.objects.get(id=post_id).likes})
            like = Like(user=request.user,publishliked = post_id)
            like.save()
            Publish.objects.get(id=post_id).likes+=1
            return JsonResponse({"message":"liked","likedNumber":Publish.objects.get(id=post_id).likes})
    return HttpResponseRedirect(reverse("index"))
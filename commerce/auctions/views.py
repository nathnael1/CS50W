from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from .models import Auctions, User, Watchlist, Bidding


def index(request):
    return render(request, "auctions/index.html",{
        "auctions": Auctions.objects.all()
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
def listing(request):
    if request.method == "GET":
        return render(request,"auctions/listing.html")
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        imageurl = request.POST["imageurl"]
        category = request.POST["category"]
        starting_bid = request.POST["starting_bid"]
        
        auction = Auctions(
            title = title,
            description = description,
            imageurl = imageurl,
            category = category,
            starting_bid = starting_bid,
            user = request.user
        )
        auction.save()
        return render(request,"auctions/index.html",{
            "message": "Auction created sucesfully",
            "auctions": Auctions.objects.all()
        })
def modify(request,auction_id):
    if request.method == "GET":
        return render(request,"auctions/modify.html",{
            "auction": Auctions.objects.get(pk=auction_id),
            "user": request.user
        })
    else:
        return "TODO"
def close(request,auction_id):
    pass
def bid(request,auction_id):
    pass
def watchlist(request,auction_id):
    if request.method =="POST":
        user = get_object_or_404(User,username = request.user)
        watchlistchecker = Watchlist.objects.filter(user = user,auction = Auctions.objects.get(pk=auction_id))
        if watchlistchecker:
            return render(request,"auctions/index.html",{
                "auctions": Auctions.objects.all(),
                "message": "already added to the watchlist"
            })
        watchlist = Watchlist(
            user = request.user,
            auction = Auctions.objects.get(pk=auction_id)
        )
        watchlist.save()
        return render(request,"auctions/index.html",{
            "auctions": Auctions.objects.all(),
            "message": "sucesfully added to the watchlist"
        })
    # for the get method the auction_id is passed as a username
    user = get_object_or_404(User,username = auction_id)
    watchlist = Watchlist.objects.filter(user = user)
    auctions = [item.auction for item in watchlist]
    return render(request,"auctions/watchlist.html",{
        "auctions":auctions
    })
def deleteWatchlist(request,auction_id):
    if request.method == "POST":
        auction = get_object_or_404(Auctions,pk = auction_id)
        watchlist = Watchlist.objects.filter(auction = auction,user = request.user)
        watchlist.delete()
        return render(request,"auctions/index.html",{
            "auctions": Auctions.objects.all(),
            "message": "sucesfully removed from the watchlist"
        })
def bidding(request,auction_id):
    if request.method == "POST":
        auction = get_object_or_404(Auctions,pk = auction_id)
        bid = int(request.POST["bid"] )
        if auction.starting_bid > bid:
            return render(request,"auctions/index.html",{
                "auctions": Auctions.objects.all(),
                "message": f"Failure: The minimum amount of bid is {auction.starting_bid}"
            })
        biddingChecker = Bidding.objects.filter(auction = auction)
        if biddingChecker:
            return render(request,"auctions/index.html",{
                "auctions":Auctions.objects.all(),
                "message": "you can't dublicate a bid"
            })
        bidding = Bidding( user = request.user, auction = auction, bid = bid)
        bidding.save()
        bidding = Bidding.objects.filter(user = request.user)
        auction = [item.auction for item in bidding]
        total = sum(item.bid for item in bidding)
        
        return render(request,"auctions/bidding.html",{
            "auctions":auction,
            "total":total,
            "message": "Bid sucessfully submitted"
        })
    else:
        user = get_object_or_404(User,username = auction_id)
        bidding = Bidding.objects.filter(user = user)
        total = sum(item.bid for item in bidding)
        auctions = [item.auction for item in bidding]
        return render(request,"auctions/bidding.html",{ "auctions": auctions,"total":total})
def bidDeletion(request,auction_id):
    if request.method == "POST":
        auction = get_object_or_404(Auctions,pk = auction_id)
        bid = Bidding.objects.filter(auction = auction,user = request.user)
        bid.delete()
        return render(request,"auctions/index.html",{
            "auctions": Auctions.objects.all(),
            "message": "Bid removed sucesfully"
           
        })

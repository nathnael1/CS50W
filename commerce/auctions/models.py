from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass
class Auctions(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=64)
    imageurl = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions",default=settings.DEFAULT_USER_ID)
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    auction = models.ForeignKey(Auctions, on_delete=models.CASCADE, related_name="watchlist")
class Bidding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidding")
    auction = models.ForeignKey(Auctions, on_delete=models.CASCADE, related_name="bidding")
    bid = models.DecimalField(max_digits=10, decimal_places=2)
class Winners(models.Model):
    auction = models.ForeignKey(Auctions, on_delete=models.SET_NULL, related_name="winner", null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="winner", null=True)
    auction_title = models.CharField(max_length=64,default=settings.DEFAULT_ACTION_TITLE)

    
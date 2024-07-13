from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
class Auctions(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=64)
    imageurl = models.URLField()
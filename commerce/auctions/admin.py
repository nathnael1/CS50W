from django.contrib import admin
from .models import User, Auctions, Watchlist, Bidding, Winners

# Register your models here.
admin.site.register(User)
admin.site.register(Auctions)
admin.site.register(Watchlist)
admin.site.register(Bidding)
admin.site.register(Winners)
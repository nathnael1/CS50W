from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing",views.listing,name = "listing"),
    path("modify/<int:auction_id>",views.modify,name = "modify"),
    path("delete/<int:auction_id>",views.delete,name ="delete"),
    path("bid/<int:auction_id>",views.bid,name = "bid"),
    path("watchlist/<int:auction_id>",views.watchlist,name = "watchlist")
]

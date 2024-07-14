from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing",views.listing,name = "listing"),
    path("modify/<int:auction_id>",views.modify,name = "modify"),
    path("close/<int:auction_id>",views.close,name ="close"),
    path("bid/<str:auction_id>",views.bidding,name = "bid"),
    path("watchlist/<str:auction_id>",views.watchlist,name = "watchlist"),
    path("watchlist/delete/<str:auction_id>",views.deleteWatchlist, name = "deleteWatchlist"),
    path("bid/delete/<str:auction_id>",views.bidDeletion,name = "bidDeletion"),
    path("comment/<str:auction_id>",views.comment,name = "comment"),
    path("category",views.category,name = "category")
]

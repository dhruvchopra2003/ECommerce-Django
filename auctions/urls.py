from django.urls import path

from . import views

app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newListing", views.newListing, name="newListing"),
    path("<int:ListingId>", views.listingPage, name="listingPage"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("closeListing", views.closeListing, name="closeListing"),
    path("victories", views.victories, name="victories"),
    path("<int:ListingId>/comments", views.comments, name="comments"),
]

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import User
from .backup import *


def index(request):
    listings = Listings.objects.filter(active=True)

    categories = Listings.objects.values_list("category").distinct()
    category_list = [category[0] for category in categories]
    print(category_list)

    category = request.GET.get("q")
    print(category)

    if category:
        listings = listings.filter(category=category)

    return render(
        request,
        "auctions/index.html",
        {
            "listings": listings,
            "category_list": category_list,
        },
    )


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def newListing(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST["description"]
        image_url = request.POST["image_url"]
        category = request.POST["category"]
        owner = User.objects.get(username=request.user.username)

        price = request.POST["price"]

        New_entry = Listings(
            title=title,
            description=description,
            img_url=image_url,
            category=category,
            owner=owner,
        )
        New_entry.save()

        current_bid = Bids(
            listing=New_entry,
            current_bid=price,
            bidder=owner,
        )
        current_bid.save()

        return HttpResponseRedirect(reverse("auctions:watchlist"))
        # return HttpResponseRedirect(reverse("auctions:index"))

    return render(request, "auctions/newListing.html")


@login_required
def listingPage(request, ListingId):
    try:
        listing = Listings.objects.get(id=ListingId)
    except:
        return HttpResponseRedirect(reverse("auctions:index"))
    # Getting the listing
    # listing = get_object_or_404(Listings, title=Title)

    # Getting the bid on the product
    bid = Bids.objects.get(listing=listing)

    # The owner/bidder of the product
    bidder = User.objects.get(username=request.user.username)

    price = bid.current_bid
    formatted_price = f"{price:,}"

    # Getting the current watchlist
    flag = False
    message = None
    current_watchlist = WatchList.objects.filter(user=request.user)
    for query_set in current_watchlist:
        if query_set.listing == ListingId:
            flag = True

    # Form handling for a new bid
    if request.method == "POST" and request.POST["form_id"] == "bid_form":
        price_offered = request.POST["bid_price"]
        print(f"{bidder} has bid ${price_offered} on {listing}")

        if float(price_offered) >= float(price):
            bid.current_bid = price_offered
            bid.bidder = bidder
            bid.save()
            print("Added new value to db")

            # Adding to the watchlist:
            if not flag:
                watchlist_entry = WatchList(user=request.user, listing=listing.id)
                watchlist_entry.save()
                print("Also Added to Watchlist")
            else:
                print("Already in watchlist")
            message = 1

        else:
            message = 0

    price = bid.current_bid
    # formatted_price = f"{price:,}"
    return render(
        request,
        "auctions/listingPage.html",
        {
            "listing": listing,
            "bid": bid,
            "price": price,
            "flag": flag,
            "message": message,
        },
    )


@login_required
def watchlist(request):

    # Elements of my_watchlist are: user(ForeignKey) and listing(characterField having the idices to the lisitngs)
    if request.method == "POST" and request.POST["form_id"] == "add":
        current_watchlist = WatchList.objects.filter(user=request.user)
        ListingId = int(request.POST["ListingId"])

        if ListingId not in [
            watchlist_entry.listing for watchlist_entry in current_watchlist
        ]:
            # Add listing to watchlist as it wasn't found
            watchlist_entry = WatchList(user=request.user, listing=ListingId)
            watchlist_entry.save()
            print("Also Added to Watchlist")
            return HttpResponseRedirect(reverse("auctions:watchlist"))
        else:
            print("Already in watchlist")
            return HttpResponseRedirect(
                reverse("auctions:listingPage", args=(ListingId,))
            )
    elif request.method == "POST" and request.POST["form_id"] == "remove":
        current_watchlist = WatchList.objects.filter(user=request.user)
        ListingId = int(request.POST["ListingId"])

        if ListingId in [
            watchlist_entry.listing for watchlist_entry in current_watchlist
        ]:
            # Add listing to watchlist as it wasn't found
            # watchlist_entry = WatchList(user=request.user, listing=ListingId)
            watchlist_entry = WatchList.objects.get(
                user=request.user, listing=ListingId
            )
            watchlist_entry.delete()
            print("Removed from Watchlist")
            return HttpResponseRedirect(reverse("auctions:watchlist"))
        else:
            print("Not in watchlist")
            return HttpResponseRedirect(
                reverse("auctions:listingPage", args=(ListingId,))
            )

    owner = request.user
    my_listings = Listings.objects.filter(owner=owner)
    my_watchlist = WatchList.objects.filter(user=owner)

    watchlist_listings = []
    for listing in my_watchlist:
        watchlist_listings.append(Listings.objects.get(pk=listing.listing))

    return render(
        request,
        "auctions/watchlist.html",
        {
            "my_bids": my_listings,
            "my_watchlist": watchlist_listings,
            # "Info": "Added to Watchlist",
        },
    )


@login_required
def closeListing(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        listing = Listings.objects.get(pk=listing_id)
        listing.active = False
        listing.save()
        print(f"saved {listing}")
        return HttpResponseRedirect(reverse("auctions:index"))


@login_required
def victories(request):
    closed_listings = Bids.objects.filter(listing__active=False, bidder=request.user)

    # print(closed_listings[0].listing.title)
    return render(
        request,
        "auctions/victories.html",
        {
            "closed_listings": closed_listings,
        },
    )


def comments(request, ListingId):
    listing = Listings.objects.get(pk=ListingId)
    commenter = request.user

    if request.method == "POST":
        comment = request.POST["comment"]
        new_comment = Comments(commenter=commenter, comment=comment, listing=listing)
        new_comment.save()

    comment_list = Comments.objects.filter(listing=listing)
    return render(
        request,
        "auctions/commentsPage.html",
        {
            "current_listing_id" : ListingId,
            "comment_list": comment_list,
        },
    )

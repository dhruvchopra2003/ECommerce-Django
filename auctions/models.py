from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listings(models.Model):
    # To store the individual listings
    title = models.CharField(max_length=64)
    description = models.TextField()
    img_url = models.URLField(null=True, blank=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="Seller",
    )
    category = models.CharField(max_length=12)
    active = models.BooleanField(default=True)

    def __str__(self):
        return (
            f"{self.title} by {self.owner} | Category: {self.category} | {self.active}"
        )


class Bids(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    # Can try OneToOneField()
    current_bid = models.FloatField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.listing} bid by {self.bidder} at ${self.current_bid}"


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.IntegerField()  # Stores the listing Id's
    # listing = models.ManyToManyField(Listings, blank=True, related_name="watchlist")


class Comments(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    comment = models.TextField()

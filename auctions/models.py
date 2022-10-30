from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Comments():
    pass

class AuctionListing(models.Model):
    #name,StartingBid,Image,Description,Categories
    #owner
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    starting_bid = models.IntegerField()
    image = models.URLField()
    categories = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.id},{self.name} ,{self.description} ,{self.starting_bid} " 

class Bids():
    pass
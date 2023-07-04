from django.contrib.auth.models import AbstractUser
from django.db import models

# categories = ["Fashion", "Toys", "Electronic", "Home"]

class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    categories = [
        ("Fashion", "Fashion"), 
        ("Toys", "Toys"),
        ("Electronic", "Electronic"),
        ("Home","Home"),
        ("Food","Food"),
    ]

    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=5000)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=15)
    category = models.CharField(blank=True,max_length=64, choices=categories)
    image = models.ImageField(blank=True,upload_to="image")
    active = models.BooleanField()
    created = models.DateTimeField()
    createdby = models.ForeignKey(User,verbose_name="createdby",on_delete=models.CASCADE)
   
    def __str__(self) -> str:
        return f"id:{self.id}, title:{self.id}, description:{self.description}, starting bid:{self.starting_bid}, active:{self.active} "
    

class WatchListModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="userwatchlist")
    auctionlisting = models.ForeignKey(AuctionListing,on_delete=models.CASCADE, related_name="userauctionlisting")
    
    def __str__(self) -> str:
        return f"id:{self.id}, user:{self.user}, {self.auctionlisting}"

class AuctionBidsModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    highestbid = models.DecimalField(decimal_places=2, max_digits=15)
    highestbiduser = models.ForeignKey(User,on_delete=models.CASCADE, related_name="highestbiduser")
    biditem = models.ForeignKey(AuctionListing,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"id:{self.id},highestbid: {self.highestbid}, by:{self.highestbiduser} on item:{self.biditem}"
    
class CommentsModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    commentby = models.ForeignKey(User,on_delete=models.CASCADE, related_name="usercomments")
    comment = models.CharField(max_length=5000)
    item = models.ForeignKey(AuctionListing,on_delete=models.CASCADE, default=1)



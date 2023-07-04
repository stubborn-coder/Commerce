from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django import forms
from django.utils import timezone
import pytz

from .models import *

def index(request):
    listings = AuctionListing.objects.all()
    return render(request, "auctions/index.html", {
        "listings":listings,
        "media_url": settings.MEDIA_URL,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
@login_required
def create_auction(request):

    if request.method == 'POST':
        print('post')
        if request.FILES.get('image',False):
            form = CreateAuctionForm(request.POST, request.FILES)
            if form.is_valid():
                print("form is valid")
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                startingbid = form.cleaned_data['starting_bid']
                category = form.cleaned_data['category']
                active = form.cleaned_data['active']
                

                upload = request.FILES.get('image',False)
                fss = FileSystemStorage()
                file = fss.save(upload.name, upload)
                print(file)
                
                
                entry = AuctionListing(title=title,description=description,starting_bid=startingbid,category=category,active=True,createdby=request.user, image=file,created=timezone.now())
                entry.save()
                bidentry = AuctionBidsModel(highestbid=startingbid,highestbiduser= request.user, biditem = entry)
                bidentry.save()
                return HttpResponseRedirect(reverse("index"))
        else:
            form = CreateAuctionForm(request.POST)
            if form.is_valid():
                
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                startingbid = form.cleaned_data['starting_bid']
                category = form.cleaned_data['category']
                active = form.cleaned_data['active']
                
        
                entry = AuctionListing(title=title,description=description,starting_bid=startingbid,category=category,active=True,createdby=request.user, image=None,created=timezone.now())
                entry.save()
                bidentry = AuctionBidsModel(highestbid=startingbid,highestbiduser= request.user, biditem = entry)
                bidentry.save()
                return HttpResponseRedirect(reverse("index"))
        
    else:

        return render(request,"auctions/create_auction.html", {
            "create_form" : CreateAuctionForm()
        })

@login_required
def watchlist(request):
    current_user = User.objects.get(id = request.user.id)
    print(current_user)
    watchlist_entries = current_user.userwatchlist.all()
    print(watchlist_entries)

    return render(request,"auctions/watchlist.html",{
        "watchlists": watchlist_entries,
    })


def listing(request,listing_id):
    list_item = AuctionListing.objects.get(id=listing_id)
    current_user = User.objects.get(id =request.user.id)
    watchlist_entries = current_user.userwatchlist.all()
    exists = watchlist_entries.filter(auctionlisting = list_item)
    owner = request.user == list_item.createdby
    bidinfo = AuctionBidsModel.objects.filter(biditem=list_item)
    bidinfo = bidinfo.first()
    print(bidinfo)
    comments = CommentsModel.objects.filter(item = list_item)
    return render(request,"auctions/listing.html", {
        "listing": list_item,
        "media_url": settings.MEDIA_URL,
        "exists": exists,
        "bidform": BidForm(),
        "owner": owner,
        "bidinfo":bidinfo,
        "comments":comments,
        "commentform":CommentForm(),

    })

@login_required
def addtowatchlist(request,listing_id):
    if request.method == "POST":
        print("adding to watch list")
        form = CreateAuctionForm(request.POST)
        print(form.is_valid())
        if form.is_valid:
            listing = AuctionListing.objects.get(id=listing_id)
            entry = WatchListModel(auctionlisting = listing, user = request.user)
            entry.save()
            print(entry)  

            return HttpResponseRedirect(reverse("listing", args=[listing_id]))
        
@login_required
def removefromwatchlist(request,listing_id):
    if request.method == "POST":
        print("removing from watch list")
        form = CreateAuctionForm(request.POST)
        
        if form.is_valid:
            list_item = AuctionListing.objects.get(id=listing_id)
            current_user = User.objects.get(id = request.user.id)
            watchlist_entries = current_user.userwatchlist.all()
            watchlist_entry = watchlist_entries.filter(auctionlisting = list_item)
            print(watchlist_entries)
            WatchListModel.objects.get(id = watchlist_entry.first().id).delete()
            return HttpResponseRedirect(reverse("listing", args=[listing_id]))
        
    
    return HttpResponseRedirect(reverse("watchlist"))
            
@login_required
def placebid(request,listing_id):
    
    if request.method == "POST":
        print("place bid post")
        form = BidForm(request.POST)

        if form.is_valid():
            print("form is valid")
            bid = form.cleaned_data["place_bid"]
            print(bid)
            listing = AuctionListing.objects.get(id=listing_id)
            current_bid = AuctionBidsModel.objects.get(biditem=listing)


            if listing:
                if bid > listing.starting_bid:
                    if bid > current_bid.highestbid:
                        current_bid.highestbid = bid
                        current_bid.highestbiduser = request.user
                        current_bid.save()
                    

            

        #return render(request,"auctions/index.html")
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))

def category(request):
    
    categories = ["Fashion", "Toys", "Electronic", "Home","Food"]
    
    return render(request,"auctions/categories.html", {
        "categories": categories,
    })

def filter(request,filter):
    categories = ["Fashion", "Toys", "Electronic", "Home","Food"]

    if filter not in categories:
        print("invalid category")
        return render(request,"auctions/index.html")
    
    listings = AuctionListing.objects.filter(category=filter)

    return render(request,"auctions/category.html",
    {
        "listings":listings,
        "category":filter,
    })
    
@login_required
def closelisting(request,listing_id):
    print("close")
    listing = AuctionListing.objects.get(id=listing_id)
    print(listing)
    if request.user == listing.createdby:
        if not listing:
            print("does not exist")
        else:
            if listing.active:
                print("change to false")
                print(listing)
                listing.active = False
                listing.save()
                print(AuctionListing.objects.filter(id=listing_id))

    return HttpResponseRedirect(reverse("listing", args=[listing_id]))

@login_required
def addcomment(request,listing_id):
    print("add comment")
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.cleaned_data['comment']
        list_item = AuctionListing.objects.get(id= listing_id)
        entry = CommentsModel(commentby= request.user, comment= comment, item = list_item)
        entry.save()
    
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))



class CreateAuctionForm(forms.Form):
    categories = [
        ("Fashion", "Fashion"), 
        ("Toys", "Toys"),
        ("Electronic", "Electronic"),
        ("Home","Home"),
        ("Food","Food"),
    ]
    
    title = forms.CharField(max_length=64,widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(max_length=5000,widget=forms.Textarea(attrs={'class': 'form-control'}))
    starting_bid = forms.DecimalField(decimal_places=2, max_digits=15, min_value=0.01,widget=forms.NumberInput(attrs={'class': 'form-control'}))
    category = forms.ChoiceField(choices=categories,required=False,widget=forms.Select(attrs={'class': 'form-control'}))
    image = forms.ImageField(required=False)
    active = forms.BooleanField(initial=True,disabled=True,widget=forms.HiddenInput(attrs={'class': 'form-control'}))
    #created = forms.DateTimeField(initial=datetime.datetime.now(),disabled=True,widget=forms.DateTimeInput(attrs={'class': 'form-control', 'hidden' : True}))
    image.widget.attrs.update({
        'class': "form-control"
    })

class BidForm(forms.Form):
    place_bid = forms.DecimalField(decimal_places=2, max_digits=15, min_value=0.01,widget=forms.NumberInput(attrs={'class': 'form-control'}))

class CommentForm(forms.Form):
    comment = forms.CharField(max_length=64,widget=forms.TextInput(attrs={'class': 'form-control'}))
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.text import slugify

from .models import User, Listing, Watchlist, Category
from .forms import ListingForm
from .functions import USD_format


def index(request):
    query = request.GET.get("q")
    if query:
        listings = Listing.objects.filter(name__icontains=query)
    else:
        listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        'listings': listings
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


def listing_detail_view(request, pk):
    listing = Listing.objects.get(pk=pk)
    form = ListingForm(instance=listing)
    if request.user.is_authenticated:
        watchlist, created = Watchlist.objects.get_or_create(user=request.user)
        if listing:
            is_watchlist = listing in watchlist.listing.all()
            return render(request, "auctions/listing.html", {
                'listing': listing,
                'is_watchlist': is_watchlist,
                'form': form
            })
    else:
        return render(request, "auctions/listing.html", {
                'listing': listing
            })
    
    
def add_watchlist(request):
    if request.method == "POST":
            user = request.user
            listing_id = request.POST["listing_id"]
            
            if listing_id:
                # Get the listing object
                listing = Listing.objects.get(pk=listing_id)
                if listing:
                    # Get or create watchlist
                    watchlist, created = Watchlist.objects.get_or_create(user=user)
                    watchlist.listing.add(listing)
                    return redirect("listing_detail", pk=listing_id)
                
            return redirect("listing_detail", pk=listing_id)
    else:           
        return redirect("index")


def remove_watchlist(request):
    if request.method == "POST":
            user = request.user
            listing_id = request.POST["listing_id"]
            
            if listing_id:
                # Get the listing object
                listing = Listing.objects.get(pk=listing_id)
                if listing:
                    # Get or create watchlist
                    watchlist, created = Watchlist.objects.get_or_create(user=user)
                    watchlist.listing.remove(listing)
                    return redirect("listing_detail", pk=listing_id)
                
            return redirect("listing_detail", pk=listing_id)
    else:           
        return redirect("index")


def watchlist(request):
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    return render(request, "auctions/watchlist.html", {
        'listings': watchlist.listing.all()
    })


def create(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.lister = request.user
            listing.save()
            return redirect("index")
    else:
        form = ListingForm()
    return render(request, "auctions/create.html", {
        'form': form
    })
    
def edit(request, pk):
    listing = get_object_or_404(Listing, pk=pk)

    if request.method == "POST":
        if request.user == listing.lister:
            form = ListingForm(request.POST, instance=listing)
            if form.is_valid():
                form.save()
                return redirect("listing_detail", pk=pk)
        else:
            return redirect("listing_detail", pk=pk)
    else:
        if request.user == listing.lister:
            form = ListingForm(instance=listing)
            return render(request, "edit_listing.html", {
                "form": form,
                "listing": listing
            })
        else:
            return redirect("listing_detail", pk=pk)

    return redirect("listing_detaill", pk=pk)
 
 
def category(request):
    categories = Category.objects.all()
    return render(request, "auctions/category_view.html", {
        'categories': categories
    })
    
    
def new_category(request):
    if request.method == "POST":
        listing = request.POST["listing"]
        name = request.POST["name"]
        slug = slugify(name)
        try:
            category = Category(name=name, slug=slug)
            category.save()
        except IntegrityError:
            return redirect("listing_detail", pk=listing)
    return redirect("listing_detail", pk=listing)
    
    
def add_category(request):
    if request.method == "POST":
        listing_id = request.POST.get("listing")
        category_id = request.POST.get("category")

        if not listing_id or not category_id:
            return redirect("index")

        try:
            listing = Listing.objects.get(pk=listing_id)
            category = Category.objects.get(pk=category_id)
        except Listing.DoesNotExist:
            return redirect("listing_detail", pk=listing_id)
        except Category.DoesNotExist:
            return redirect("listing_detail", pk=listing_id)

        category.listing.add(listing)
        return redirect("listing_detail", pk=listing_id)

    return redirect("index")
        
    
def category_view(request, slug):
    category = Category.objects.get(slug=slug)
    return render(request, "auctions/category_view.html", {
        'listings': category.listing.all()
    })
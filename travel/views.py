import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import Http404
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.forms import modelformset_factory
from django.contrib import messages
from django.db.models import Q

from .models import *
from .forms import *
from datetime import date


def index(request):
    today = datetime.datetime.today()
    if request.GET.get('search'):
        search = request.GET.get('search')
        all = Place.objects.all()
        places = Place.objects.filter(city=search).order_by("-created_date")
    else:
        places = Place.objects.all().order_by("-created_date")
    paginator = Paginator(places, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    

    return render(request, "travel/index.html", {
        "page_obj": page_obj,
        "today": today
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
            return render(request, "travel/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "travel/login.html")


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
            return render(request, "travel/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "travel/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "travel/register.html")


@login_required(login_url="login")
def host(request):
    if request.method == "POST": 
        post = request.POST.copy()
        post["user"] = User.objects.get(pk=request.user.id)
        form = ImageForm(post, request.FILES or None )
        files = request.FILES.getlist('image')
        
        if form.is_valid():
            place_form = form.save(commit=False)
            place_form.save()
                
            for f in files:
                photo = Images(place=place_form, image=f)
                photo.save()
            messages.success(request, 'Your place got hosted successfully !')
            return HttpResponseRedirect(reverse("properties"))

        return render(request, "travel/host.html", {
            "form": form,
            "messages": form.errors.as_data
        })
    return render(request, "travel/host.html", {
        "form": ImageForm()
    })
    

def place(request, id):
    place = Place.objects.get(pk=id)
    images = place.images_set.all()
    saved = False
    customer = Customer.objects.filter(user=request.user,place=place)
    get_customer = customer.first()
    get_d_customer =  Customer.objects.filter(place=place).first()
    
    if request.user.is_authenticated:
        if hasattr(request.user, 'saved') and request.user.saved.places.filter(pk=place.id).exists():
            saved = True

    if request.method == "POST":
        if request.user.is_authenticated:
            if request.POST["type"] == "comment":
                if not request.POST["content"]:
                    return render(request, "travel/place.html", {
                        "place": place,
                        "saved": saved,
                        "comment_error": "Content is required"
                    })
    
                comment = Comment(
                    user = User.objects.get(pk=request.user.id),
                    place = place,
                    comment = request.POST["content"]
                )

                comment.save()
                return HttpResponseRedirect(reverse("place", args=[place.id]))
            
            elif request.POST["type"] == "book":
                book_user = Customer(
                    user = User.objects.get(pk=request.user.id),
                    place = place,
                    guests = request.POST["guests"],
                    checkin_date = request.POST["checkin"],
                    checkout_date = request.POST["checkout"]
                )
                book_user.save()
                place.available = False
                place.save()
                return HttpResponseRedirect(reverse("payment", args=[place.id]))
            
            elif request.POST["type"] == "payment":
                messages.success(request, 'Your booking was successful !')
                return HttpResponseRedirect(reverse("trips"))
            
            elif request.POST["type"] == "edit":
                form = ImageForm(initial=model_to_dict(place))
                
                return render(request, "travel/host.html", {
                    "form1": form,
                    "place_id": place.id
                }) 

            elif request.POST["type"] == "close":
                if customer:
                    customer.delete()
                place.available = True
                place.save()
                return HttpResponseRedirect(reverse("place", args=[place.id]))
            
            elif request.POST["type"] == "delete":
                place.delete()
                return HttpResponseRedirect(reverse("index"))
            
            elif request.POST["type"] == "save":
                if saved:
                    places = request.user.saved.places
                    places.remove(place)
                else:
                    if not hasattr(request.user, 'saved'):
                        request.user.saved = Saved()
                        request.user.saved.save()
                    
                    places = request.user.saved.places
                    places.add(place)
                return HttpResponseRedirect(reverse("place", args=[place.id]))
        else:
            messages.warning(request, 'Log in to book property,  host property and more!')
            return HttpResponseRedirect(reverse("place", args=[place.id]))

    return render(request, "travel/place.html", {
        "place": place,
        "saved": saved,
        "customer":get_customer,
        "images": images,
        "customer1": get_d_customer
    })

def trips(request):
    places = []
    trips = Customer.objects.filter(user=request.user)
    if trips:
        if request.GET.get('search'):
            search = request.GET.get('search')
            for trip in trips:
                places += Place.objects.filter(id=trip.place.id, city=search).order_by("-created_date")
        else:
            for trip in trips:
                places += Place.objects.filter(id=trip.place.id).order_by("-created_date")

        paginator = Paginator(places, 9)
        page_obj = paginator.get_page(request.GET.get('page'))
        return render(request, "travel/index.html", {
            "page_obj": page_obj
        })
    else:
        messages.warning(request, "You haven't booked any place yet :(")
        return HttpResponseRedirect(reverse("index"))

def properties(request):
    properties = Place.objects.filter(user=request.user)
    if properties:
        if request.GET.get('search'):
            search = request.GET.get('search')
            places = Place.objects.filter(city=search, user=request.user).order_by("-created_date")
        else:
            places = properties.order_by("-created_date")
        
        paginator = Paginator(places, 9)
        page_obj = paginator.get_page(request.GET.get('page'))
        return render(request, "travel/index.html", {
            "page_obj": page_obj
        })
    else:
        messages.warning(request, "You haven't hosted any place yet :(")
        return HttpResponseRedirect(reverse("index"))

def saved(request):
    saved = request.user.saved.places.all()
    if saved:
        places = saved.order_by("-created_date")
        paginator = Paginator(places, 9)
        page_obj = paginator.get_page(request.GET.get('page'))
        return render(request, "travel/index.html", {
            "page_obj": page_obj
        })   
    
    messages.warning(request, "You haven't saved any place yet :(")
    return HttpResponseRedirect(reverse("index"))

def payment(request,id):
    if request.method =="POST":
        raise Http404("Can't be accessed in POST request")
    else:
        return render(request, "travel/payment.html",{
            "place_id":id
        })

def edit(request,id):
    if request.method == 'POST':
        if request.user.places.filter(pk=id).exists():
            place = Place.objects.filter(id=id,user=request.user)
            place.delete()
            
            post = request.POST.copy()
            post["user"] = User.objects.get(pk=request.user.id)
            form = ImageForm(post, request.FILES or None)
            files = request.FILES.getlist('image')
            if form.is_valid():
                place_form = form.save(commit=False)
                place_form.save()

            for f in files:
                photo = Images(place=place_form, image=f)
                photo.save()
            
            messages.success(request, 'Your property has been updated!')
            return HttpResponseRedirect(reverse("properties"))

        else:
            return render(request, "travel/host.html", {
                "form": form,
                "messages": form.errors.as_data
            })
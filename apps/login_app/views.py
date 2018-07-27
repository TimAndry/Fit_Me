from django.shortcuts import render, redirect
#used to import messages
from django.contrib import messages
from .models import *
import re, bcrypt
from django.db.models import Q
from geopy.geocoders import Nominatim
from geopy import geocoders
from geopy.exc import GeocoderTimedOut
#added q import for easier queryset management


geolocator = Nominatim()
g = geocoders.GoogleV3(api_key='AIzaSyAlh4cKb_0NhmjwAdrKk9xoGa1Usm7LwZQ')

#use regualr expression to validate email
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#looks for one number
NAME_REGEX = re.compile(r'[0-9]')
#looks for one lower case, one upper case, and one number
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)')

def index(request):
    place = Place.objects.all()
    context  = {
        'place': place
    }
    return render(request, 'login_app/index.html', context)

def registration(request):
    result = User.objects.validate_registration(request.POST)
    if len(result) > 0:
        for key in result.keys():
            print(result[key])
            messages.error(request, result[key], extra_tags = key)
    else:
        #hash the password
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        
        user = User.objects.create(first_name = request.POST['fname'], last_name = request.POST['lname'], password = hashed_pw, email = request.POST['email'])
        #creates a user instance

        friend = Friend.objects.create(first_name = request.POST['fname'], last_name = request.POST['lname'], email = request.POST['email'])
        #uses the registration information to add that name to the friend database

        request.session['user_id'] = user.id
        return redirect('user/' + str(request.session['user_id']))
    return redirect('/')

def login(request):
    user = User.objects.filter(email = request.POST['email'])
    if len(user) == 0:
        messages.error(request, 'This user does not exist', extra_tags = 'email')
        return redirect('/')
    else:
        user = user.first()
    #Checks if passwords are valid .checkpw
    valid_pass = bcrypt.checkpw(request.POST['pass2word'].encode(), user.password.encode())
    if request.POST['pass2word'] == "":
        messages.error( request, 'enter a valid password', extra_tags = 'pass2word')
    if valid_pass:
        request.session['user_id'] = user.id
        messages.error( request, user.first_name + ' is now logged in', extra_tags = 'email')
        print(user.first_name)
        return redirect('user/' + str(request.session['user_id']))
    else:
        messages.error( request, 'This password email combination was not found', extra_tags = 'email')
    return redirect('/')

def home(request, user_id):
    curr_user = User.objects.get(id = request.session['user_id'])
    all_places = Place.objects.all()
    friends = Friend.objects.filter(of_user = request.session['user_id'])
    latlong = Place.objects.get(id = 9)
    my_places = Place.objects.filter(is_going = request.session['user_id'])
    other_places = Place.objects.filter(~Q(is_going = request.session['user_id']))
    print(other_places)
    context = {
        'user':curr_user,
        'place':all_places,
        'friends': friends,
        'latlong': latlong,
        'my_places': my_places,
        'other_places': other_places,
    }
    return render(request, 'login_app/home.html', context)

def user(request, user_id):
    user = User.objects.get(id = request.session['user_id'])
    #gets the current user
    
    place = Place.objects.all()
    #gets a list of places

    follow = Friend.objects.filter(~Q(of_user = request.session['user_id']))

    #gets a list of all the users (later i'll use this to create a list of suggested users like User.objects.filter(some filter)

    friends = Friend.objects.filter(of_user = request.session['user_id'])
    #creates the list of friends

    going = Place.objects.filter(is_going = request.session['user_id'])
    #shows the places the user is going
    
    

    context = {
        'user':user,
        'place':place,
        'follow': follow,
        'friends': friends,
        'going': going,
    }
    
    return render(request, 'login_app/user.html', context )


def addworkout(request):
    result = User.objects.validate_place(request.POST)
    if len(result) > 0:
        for key in result.keys():
            print(result[key])
            messages.error(request, result[key], extra_tags = key)
        return redirect('user/' + str(request.session['user_id']))
    else:
        street = str(request.POST['street'])
        city =  str(request.POST['city'])
        state =  str(request.POST['state'])
        lat = street + ' ' + city + ' ' + state
        lat = g.geocode(lat)
        latcord = str(lat.latitude)
        arr=[]
        arr.append(latcord)
        print(arr[0])
        longi = (str(request.POST['street']) + ' ' + str(request.POST['city']) + ', ' + str(request.POST['state']))
        longi = g.geocode(longi)
        longcord = str(longi.longitude)
        arr2 = []
        arr2.append(longcord)
        print(arr2[0])
        
        Place.objects.create(place_name = request.POST['place_name'], street = request.POST['street'], city = request.POST['city'], state = request.POST['state'], zip_code = request.POST['zip_code'], fit_type = request.POST['fit_type'], desc = request.POST['description'], date = request.POST['date'], getlat = arr[0], getlong = arr2[0])

    return redirect('user/' + str(request.session['user_id']))


def going(request):
    is_going = User.objects.get(id = request.POST['user'])
    friend_going = Friend.objects.get(id = request.POST['user'])
    this_place = Place.objects.get(id = request.POST['place'])
    is_going.this_place.add(this_place)
    friend_going.that_place.add(this_place)
    return redirect('user/' + str(request.session['user_id']))


def follow(request):
    of_user = User.objects.get(id = request.POST['user'])
    friend = Friend.objects.get(id = request.POST['friend'])
    print(of_user.first_name, friend.first_name)
    of_user.friends.add(friend)
    return redirect('user/' + str(request.session['user_id']))

def edit(request):
    if request.method == 'POST':
        request.session['place'] = Place.objects.get(id = request.POST['edit']).id
        return redirect('/update')

def update(request):

    return render(request, 'login_app/edit.html')

def change(request):
    result = User.objects.validate_place(request.POST)
    if len(result) > 0:
         
        for key in result.keys():
            print(result[key])
            messages.error(request, result[key], extra_tags = key)
        return redirect('/edit')
    else:
        place = Place.objects.get(id = request.session['place'])
        place.place_name = request.POST['place_name']
        place.fit_type = request.POST['fit_type']
        place.desc = request.POST['description']
        place.date = request.POST['date']
        place.street = request.POSt['street']
        place.city = request.POSt['city']
        place.state = request.POSt['state']
        place.zip_code = request.POSt['zip_code']
        place.save()
        return redirect('/user/' + str(request.session['user_id']))

def cancel(request):
    cancel = Place.objects.get(id = request.POST['cancel'])
    cancel.delete()
    if 'user_id' in request.session:
        return redirect('user/' + str(request.session['user_id']))
    else: return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')
    

def showplace(request, going_id):
    friend = Friend.objects.filter(that_place = going_id)
    print(friend)
    user = User.objects.get(id = request.session['user_id'])
    here = Place.objects.get(id = going_id)
    context ={
        'friend': friend,
        'user': user,
        'here': here,
    } 
    return render(request, 'login_app/showplace.html', context)

def showuser(request, user_id):
    user = User.objects.get(id = user_id)
    places = Place.objects.filter(is_going = user_id)
    follow = Friend.objects.filter(of_user = user_id)
    context = {
        'user': user,
        'places': places,
        'follow': follow,
    }
    return render(request, 'login_app/showuser.html', context)

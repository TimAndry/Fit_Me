from django.shortcuts import render, redirect
#used to import messages
from django.contrib import messages
from .models import *
import re, bcrypt

"""

A SHORT LIST OF REGULAR EXPRESSIONS
^                  // the start of the string
(?=.*[a-z])        // use positive look ahead to see if at least one lower case letter exists
(?=.*[A-Z])        // use positive look ahead to see if at least one upper case letter exists
(?=.*\d)           // use positive look ahead to see if at least one digit exists
(?=.*[_\W])        // use positive look ahead to see if at least one underscore or non-word character exists
.+                 // gobble up the entire string
$                  // the end of the string

"""



#use regualr expression to validate email
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#looks for one number
NAME_REGEX = re.compile(r'[0-9]')
#looks for one lower case, one upper case, and one number
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)')

def index(request):
    return render(request, 'login_app/index.html')

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
        request.session['user_id'] = user.id
        return redirect('user/' + str(request.session['user_id']))
    return redirect('/')

def login(request):
    user = User.objects.filter(email = request.POST['em2ail'])
    if len(user) == 0:
        messages.error(request, 'This user does not exist', extra_tags = 'em2ail')
        return redirect('/')
    else:
        user = user.first()
    #Checks if passwords are valid .checkpw
    valid_pass = bcrypt.checkpw(request.POST['pass2word'].encode(), user.password.encode())
    if request.POST['pass2word'] == "":
        messages.error( request, 'enter a valid password', extra_tags = 'pass2word')
    if valid_pass:
        request.session['user_id'] = user.id
        messages.error( request, user.first_name + ' is now logged in', extra_tags = 'em2ail')
        print(user.first_name)
        return redirect('user/' + str(request.session['user_id']))
    else:
        messages.error( request, 'This password email combination was not found', extra_tags = 'em2ail')
    return redirect('/')


def user(request, user_id):
    user = User.objects.get(id = request.session['user_id'])
    context = {
        'user':user
    }
    return render(request, 'login_app/user.html', context)
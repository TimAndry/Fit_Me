from django.db import models
from django import forms
import re, datetime

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

#UserManager acts as a validation dictionary
class UserManager(models.Manager):
    #post_data is a dictionary that represents the request.POST information
    def validate_registration(self, post_data):
        errors = {}
        #validate if all fields are present
        if len(post_data['fname']) == 0 or NAME_REGEX.search(post_data['fname']):
            errors['fname'] = 'Must provide valid first name'
        if len(post_data['lname']) == 0 or NAME_REGEX.search(post_data['fname']):
            errors['lname'] = 'Must provide valid last name'
        if len(post_data['email']) == 0 or not EMAIL_REGEX.match(post_data['email']) :
            errors['email'] = 'Must provide valid email'
        if len(post_data['password']) < 8:
            errors['password'] = 'Must provide valid passsword (at least 8 characters in length)'
        #valid email
        emails_query = self.filter(email = post_data['email'])
        if len(emails_query) > 0:
            errors['email'] = 'email already exists'
        #passwords match
        if post_data['password'] != post_data['check_password']:
            errors['password'] = 'Passwords do not match'
        return errors
    
    def validate_login(self, post_data):
        errors = {}
        email_query = self.filter(email = post_data['email'])
        if len(email_query) == 0:
            errors['email'] = 'This user does not exist'
        return errors

    def validate_place(self, post_data):
        errors = {}
        if len(post_data['place_name']) < 2:
            errors['place_name'] = 'must be longer than 2 characters'
        if len(post_data['street']) < 3:
            errors['street'] = 'please input a valid street'
        if len(post_data['city']) < 3:
            errors['city'] = 'please provide a valid location'
        if len(post_data['zip_code']) < 5:
            errors['zip_code'] = 'please provide a valid zip'
        if len(post_data['description']) < 15:
            errors['description'] = 'please enter a longer description'
        if post_data['state'] == 'Choose State':
            errors['state'] = 'select a state'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 60)
    last_name = models.CharField(max_length = 60)
    email = models.CharField(max_length = 60)
    password = models.CharField(max_length = 255)
    #replaces objects call from user.objects.... to user.UserManager().
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Friend(models.Model):
    first_name = models.CharField(max_length = 60)
    last_name = models.CharField(max_length = 60)
    email = models.CharField(max_length = 60)
    of_user = models.ManyToManyField(User, related_name = "friends")
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Place(models.Model):
    place_name = models.CharField(max_length = 60)
    date = models.DateField()
    street = models.CharField(max_length = 60)
    city = models.CharField(max_length = 60)
    state = models.CharField(max_length = 2)
    zip_code = models.IntegerField()
    fit_type = models.CharField(max_length = 60)
    desc = models.TextField(max_length = 60)
    is_going = models.ManyToManyField(User, related_name = "this_place")
    friend_going = models.ManyToManyField(Friend, related_name = "that_place")
    getlat = models.CharField(max_length = 1000)
    getlong = models.CharField(max_length = 1000)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

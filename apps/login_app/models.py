from django.db import models
import re

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

class User(models.Model):
    first_name = models.CharField(max_length = 60)
    last_name = models.CharField(max_length = 60)
    email = models.CharField(max_length = 60)
    password = models.CharField(max_length = 255)
    #replaces objects call from user.objects.... to user.UserManager().
    objects = UserManager()

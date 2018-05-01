from __future__ import unicode_literals
from django.db import models
import bcrypt
import re 
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    #Validate registration
    def reg_validator(self, request):
        errors = []
        if len(request.POST['first_name']) < 1 and len(request.POST['last_name']) < 1:
            errors.append('First (Last) Name cannot be blank')
        if not (request.POST['first_name'].isalpha() and request.POST['last_name'].isalpha()):
            errors.append('First (Last) Name cannot contain numbers or special characters')
        if len(request.POST['handle']) < 1: 
            errors.append('Gamer Handle cannot be blank')
        if not email_regex.match(request.POST['email']):
            errors.append('Invalid email')
        if len(request.POST['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        if request.POST['confirm_password'] != request.POST['password']:
            errors.append('Passwords do not match')
        users = User.objects.all()
        # check if email/gamer handle already exists
        for user in users:
            if request.POST['email'] == user.email:
                errors.append('Email already exists')
            if request.POST['handle'] == user.handle:
                errors.append('Gamer Handle already exists')
        return errors
    #Create new user
    def reg_user(self, request):
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], handle=request.POST['handle'], email=request.POST['email'], password=hashed_pw)
    #Validate login
    def log_validator(self, request):
        errors = []
        users = User.objects.filter(email = request.POST['email'])
        if len(users) > 0:
            user = users[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['logged_id'] = user.id
                return errors
            else: 
                errors.append('Incorrect Password')
                return errors
        else: 
            errors.append('Email not found')
            return errors
    #Validate users updated email 
    def update_email_validator(self, request):
        errors = []
        if not email_regex.match(request.POST['email']):
            errors.append('Invalid email')
        users = User.objects.all()
        for user in users:
            if request.POST['email'] == user.email:
                errors.append('Email already exists')
        return errors
    #Update user email 
    def update_email(self, request):
        user = User.objects.get(id = request.session['logged_id'])
        user.email = request.POST['email']
        user.save()
    #Validate users update password
    def update_password_validator(self, request):
        errors = []
        if len(request.POST['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        if request.POST['confirm_password'] != request.POST['password']:
            errors.append('Passwords do not match')
        return errors
    #Update user password
    def update_password(self, request):
        user = User.objects.get(id = request.session['logged_id'])
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user.password = hashed_pw
        user.save()
            
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    handle = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()



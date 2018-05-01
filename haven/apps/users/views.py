from django.shortcuts import render, redirect
from django.contrib import messages
from models import User 
from ..posts.models import *

def index(request):    
    if 'logged_id' not in request.session:
        return render(request, 'users/index.html')
    else: 
        return redirect('/users/' + str(request.session['logged_id']))

def login(request):
    if 'logged_id' not in request.session:
        return render(request, 'users/login.html')
    else: 
        return redirect('/users/' + str(request.session['logged_id']))

def register(request):
    if 'logged_id' not in request.session:
        return render(request, 'users/register.html')
    else: 
        return redirect('/users/' + str(request.session['logged_id']))

def process_login(request):
    if request.method == 'POST':
        errors = User.objects.log_validator(request)
        if len(errors):
            for error in errors:
                messages.error(request, error)
                return redirect('/login')
        else:
            return redirect('/users/' + str(request.session['logged_id']))

def process_register(request):
    if request.method == 'POST':
        errors = User.objects.reg_validator(request)
        if len(errors):
            for error in errors:
                messages.error(request, error)
            return redirect('/register')
        else: 
            User.objects.reg_user(request)
            request.session['logged_id'] = User.objects.last().id
            return redirect ('/users/' + str(request.session['logged_id']))

def users(request, id):
    context = {
        'user': User.objects.get(id = id),
        'posts': Post.objects.filter(user_id = id),
        'comments': Comment.objects.all(),
    }
    return render(request, 'users/users.html', context)

def community(request):
    context = {
        'users': User.objects.all().order_by('handle')
    }
    return render(request, 'users/community.html', context)

def settings(request, id):
    context = {
        'user': User.objects.get(id = id)
    }
    return render(request, 'users/settings.html', context)

def update_email(request):
    if request.method == 'POST':
        errors = User.objects.update_email_validator(request)
        if len(errors):
            for error in errors:
                messages.error(request, error)
            return redirect('/users/' + str(request.session['logged_id']) + '/settings')
        else: 
            User.objects.update_email(request)
            messages.success(request, 'Email successfully updated!')
            return redirect('/users/' + str(request.session['logged_id']) + '/settings')

def update_password(request):
    if request.method == 'POST':
        errors = User.objects.update_password_validator(request)
        if len(errors):
            for error in errors:
                messages.error(request, error)
            return redirect('/users/' + str(request.session['logged_id']) + '/settings')
        else: 
            User.objects.update_password(request)
            messages.success(request, 'Password successfully updated!')
            return redirect('/users/' + str(request.session['logged_id']) + '/settings')

def logout(request):
    request.session.clear()
    return redirect('/')
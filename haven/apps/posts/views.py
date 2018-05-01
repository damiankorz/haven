from django.shortcuts import render, redirect
from django.contrib import messages 
from models import *

def posts(request):
    context = {
        'posts': Post.objects.recent_five_posts(request),
    }
    return render(request, 'posts/posts.html', context)

def process_post(request):
    if request.method == 'POST':
        errors = Post.objects.post_validator(request)
        if len(errors): 
            for error in errors: 
                messages.error(request, error)
            return redirect('/users/' + str(request.session['logged_id']))
        else: 
            Post.objects.create_post(request)
            return redirect('/users/' + str(request.session['logged_id']))

def comment(request, user_id, post_id):
    if request.method == 'POST': 
        errors = Comment.objects.comment_validator(request)
        if len(errors):
            for error in errors: 
                messages.error(request, error)
            return redirect('/users/' + user_id)
        else: 
            Comment.objects.create_comment(request, post_id)
            return redirect('/users/' + user_id)

def delete_comment(request, user_id, comment_id):
    Comment.objects.delete_comment(request, comment_id)
    return redirect('/users/' + user_id)
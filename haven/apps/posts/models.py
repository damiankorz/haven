from __future__ import unicode_literals
from django.db import models
from ..users.models import *

class PostManager(models.Manager):
    #Validate post content 
    def post_validator(self, request):
        errors = []
        if len(request.POST['title']) < 1:
            errors.append('Post title cannot be blank')
        if len(request.POST['post_content']) < 1:
            errors.append('Post content cannot be blank')
        return errors
    #Create post 
    def create_post(self, request):
        Post.objects.create(title=request.POST['title'], content=request.POST['post_content'], user_id=request.session['logged_id'])
    def recent_five_posts(self, request):
        recent_five = Post.objects.all().order_by('-created_at')[:5]
        return recent_five 

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    user = models.ForeignKey(User, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PostManager()

class CommentManager(models.Manager):
    def comment_validator(self, request):
        errors = []
        if len(request.POST['comment_content']) < 1:
            errors.append('Comment content cannot be blank')
        return errors
    def create_comment(self, request, post_id):
        Comment.objects.create(content=request.POST['comment_content'], post_id=post_id, user_id=request.session['logged_id'])
    def delete_comment(self, request, id):
        comment = Comment.objects.get(id = id)
        comment.delete()

class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, related_name="posts")
    user = models.ForeignKey(User, related_name="users")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()
    

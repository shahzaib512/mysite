from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404


def post_list(request):
    posts = Post.published.all()
    return render(request, 'blog/post/list.html',
                {'posts': posts})

def post_detail(request, year, month, day, plug):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=plug)
    return render(request, 'blog/post/detail.html', {'post': post})

from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def post_list(request):
    post_list = Post.published.all()
    
    # Paginator with 3 posts per page
    paginator = Paginator(post_list, 3)
    
    # Get the requested page number
    page_number = request.GET.get('page', 1)
    
    try:
        # Get the posts for the requested page
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'posts': posts})
def post_detail(request, year, month, day, plug):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=plug)
    return render(request, 'blog/post/detail.html', {'post': post})

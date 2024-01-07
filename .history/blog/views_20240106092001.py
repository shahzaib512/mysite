from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView
from .forms import EmailPostForm




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

class PostListView(ListView):
    """
    Alternative post list view
    """
    
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_share(request, post_id):
    # Retrieve post by id 
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    
    if request.method == 'POST':
        # Form was submitted 
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form field passes validation
            cd = form.cleaned_data
            # .. send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                f"{cd['name']}'s comments: {cd['comments']}"
            send_email(subject, message, 'shahzaibshah0028@gmail.com',
                       [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})

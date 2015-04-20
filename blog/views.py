from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader

from blog.models import Post

from django.shortcuts import get_object_or_404

# helper functions
def encode_url(url):
    return url.replace(' ', '_')

def get_popular_posts():
    return Post.objects.order_by('-views')[:5]


def index(request):
    latest_posts = Post.objects.all().order_by('-created_at')
    t = loader.get_template('blog/index.html')
    context_dict = {
        'latest_posts': latest_posts, 
        'popular_posts': get_popular_posts(),
    }
    for post in latest_posts:
        post.url = encode_url(post.title)
    for popular_post in popular_posts:
        popular_post.url = encode_url(popular_post.title)
    c = Context(context_dict)
    return HttpResponse(t.render(c))


def post(request, post_url):
    single_post = get_object_or_404(Post, title=post_url.replace('_',' '))
    single_post.views += 1
    single_post.save()
    for popular_post in popular_posts:
        popular_post.url = encode_url(popular_post.title)
    t = loader.get_template('blog/post.html')
    context_dict = {
        'single_post': single_post, 
        'popular_posts': get_popular_posts(), 
    }
    c = Context(context_dict)
    return HttpResponse(t.render(c))
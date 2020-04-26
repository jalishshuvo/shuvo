from django.shortcuts import render,get_object_or_404,redirect,reverse

from .models import Post,Author,PostView,Category
from marketing.models import SignUp
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Count,Q
from .forms import CommentForm,PostForm

def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains = query)|
            Q(overview__icontains = query)
        ).distinct()
    context={
       "queryset" : queryset
    }
    return render(request,'search_result.html',context)

def get_category_count():
    queryset = Post\
        .objects\
        .values('categories__title')\
        .annotate(Count('categories__title'))
    return queryset

def list_of_post_by_category(request,category_slug):
    categories = Category.objects.all()
    post = Post.objects.filter(status='published').order_by('-timestamp')
    if category_slug:
        categories = get_object_or_404(Category,slug= category_slug)
        post = post.filter(categories=categories)
        
    category_count = get_category_count()
    
    latest = Post.objects.filter(status='published').order_by('-timestamp')[0:3]
    post_list = Post.objects.all()
    paginator = Paginator(post_list,4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    
    template = 'list_of_post_by_category.html'
    context ={
        'categories' : categories,
        'post' : post,
        'category_count' : category_count,
        'queryset' : paginated_queryset ,
        'page_request_var' : page_request_var,
        'latest' : latest
    }
    return render(request,template,context)

def index(request):
    
    featured = Post.objects.filter(featured=True,status='published')[0:3]
    latest = Post.objects.filter(status='published').order_by('-timestamp')[0:3]

    if request.method == "POST":
        email = request.POST["email"]
        new_signup = SignUp()
        new_signup.email = email
        new_signup.save()

    context ={
        'object_list': featured,
        'latest' : latest
    }
    return render(request,'index.html',context)
def about(request):
    template='about.html'
    return render(request,template)
def privacy(request):
    template='privacy_policy.html'
    return render(request,template)



def blog(request):
    categories = Category.objects.filter()
    category_count = get_category_count()
    
    latest = Post.objects.filter(status='published').order_by('-timestamp')[0:3]
    post_list = Post.objects.filter(status='published').order_by('-timestamp')
    paginator = Paginator(post_list,6)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context= {
        'categories' : categories,
        'category_count' : category_count,
        'queryset' : paginated_queryset ,
        'page_request_var' : page_request_var,
        'latest' : latest

    }
    return render(request,'blog.html',context)



def post_detail(request, slug):

    latest = Post.objects.filter(status='published').order_by('-timestamp')[0:3]
    category_count = get_category_count()
    most_recent = Post.objects.filter(status='published').order_by('-timestamp')[:3]
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm(request.POST or None)

    # if request.user.is_authenticated:
    #     PostView.objects.get_or_create(user=request.user,post=post)

    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'slug': post.slug
            }))
    context = {
        'post': post,
        'most_recent': most_recent,
        'category_count': category_count,
        'form': form,
        'latest' : latest

    }
    return render(request, 'post.html', context)

def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author         
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'slug': form.instance.slug
            }))

    context ={
        'form': form,
        'title': title
        
    }
        
    return render(request,'post_create.html',context)

def post_update(request, slug):
    title = 'Update'
    post = get_object_or_404(Post,slug=slug)
    form = PostForm(request.POST or None, request.FILES or None,instance= post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author         
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'slug': form.instance.slug
            }))

    context ={
        'form': form,
        'title' : title
        
    }
        
    return render(request,'post_create.html',context)
def post_delete(request, slug):
    post = get_object_or_404(Post, slug = slug)
    post.delete()
    return redirect(reverse('post-list'))
from django.shortcuts import render, get_object_or_404, redirect
from .models import Content, Category, Comment
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views import generic
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully signed up.')
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Author.objects.create(name =user)
              #  messages.success(request,  ' {{user}} you have been logged in!')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please enter the correct fields.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')
def home(request):
    return render(request, 'index.html')

def index(request):
    posts = Content.objects.all()
    paginator = Paginator(posts,3)
    page_number = request.GET.get('page',1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        #if page is not an integer 
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {'posts': posts,}
    return render(request, 'post.html', context)

def posting(request, id):
    begin = Content.objects.get(id=id)
    res = Comment.objects.all()
    req = CommentForm()
    if request.method=='POST':
       req=CommentForm(request.POST)
       if req.is_valid():
           post = begin
           username = request.user
           email = request.POST.get('email')
           text = request.POST.get('text')
           Comment.objects.create(post = post, username = username, email=email, text = text)
    else:
        req = CommentForm()      
    return render(request, 'posted.html', {'form': begin, 'res': res,'req':req})

def update_blog(request, id):
    blog = get_object_or_404(Content, id=id)
    if request.method == 'POST':
        form = ContentForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('posting', id=id)
    else:
        form = ContentForm(instance=blog)
    return render(request, 'update_blog.html', {'form': form, 'blog': blog})
def delete_blog(request, id):
    blog = get_object_or_404(Content, id=id)
    if request.method == 'POST':
        blog.delete()
        messages.success(request, 'Blog post has been deleted successfully.')
        return redirect('index')
    return render(request, 'delete_blog.html', {'blog': blog})

def user_profile(request):
    user = request.user
    profile = Profile()
    context = {
        'user': user,
        'profile': profile  
    }
    return render(request, 'profile.html', context)
class update_profile(generic.UpdateView):
    form_class =  UserChangeForm
    template_name = "update_profile.html"
    success_url = reverse_lazy('profile')
    
    def get_object(self):
        return self.request.user

#     user = request.user
#     profile = user.profile

#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')
#     else:
#         form = ProfileForm(instance=profile)

#     context = {
#         'form': form
#     }
    
def create_post(request):
    initial_data = {
            'author': request.user.username,
            
        }    
    form =PostForm(initial= initial_data)
    
    if request.method == 'POST':

        form = PostForm(request.POST,request.FILES)

        if form.is_valid():
            
            category_id = request.POST.get('category')
            category = get_object_or_404(Category, pk=category_id)
            
            Content.objects.create(
                title = request.POST.get('title'),
                slug = request.POST.get('slug'),
                category = category,
                author = request.user,
                image = request.FILES['image'],
                content = request.POST.get('content'),
                status = request.POST.get('status')
            )
            return redirect('index')
    else:
        form = PostForm()

    context = {'form': form}
    return render(request, 'create_post.html', context)


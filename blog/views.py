from django.shortcuts import render, get_object_or_404, redirect
from .models import Content, Category, Comment
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
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
    form = Content.objects.all()
    return render(request, 'post.html', {'start': form})

def posting(request, id):
    begin = Content.objects.get(id=id)
    res = Comment.objects.all()
    req = CommentForm()
    if request.method=='POST':
       req=CommentForm(request.POST)
       if req.is_valid():
           req.save()
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
    model = User
    template_name = "update_profile.html"


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
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            # post.author = request.user.author
            post.save()
            return redirect('index')
    else:
        form = PostForm()

    context = {'form': form}
    return render(request, 'create_post.html', context)


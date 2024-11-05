
from django.http import *
from django.template import loader
from django.contrib.auth import login,authenticate,logout
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from .models import Member
from main.models import Post, Comment
from django.http import HttpResponseRedirect
from main.forms import CommentForm
from django.http import HttpResponseRedirect
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import Category
from django.contrib.auth.decorators import login_required
from .forms import ProfileImageForm
from django.shortcuts import render, redirect
from .forms import ProfileImageForm
from .models import Post, CustomUser
from django.views.generic import ListView
from .models import Category, Post




def main(request):
  mymembers = Member.objects.all().values()
  template = loader.get_template('main.html')
  context = {
    'mymembers': mymembers,
  }
  return HttpResponse(template.render(context, request))
def about(request):
  template = loader.get_template('about.html')
  context = {
    'about' : about,
  }
  return HttpResponse(template.render(context, request))
def dashboard(request):
    return render(request, "dashboard.html")

class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'  # فایل قالبی که لیست دسته‌ها را نمایش می‌دهد
    context_object_name = 'categories'  # نامی که در قالب به لیست دسترسی داریم

def blog_index(request):
    latest_posts = Post.objects.order_by('-created_on')[:3]  
    other_posts = Post.objects.order_by('-created_on')[3:]   
    
    context = {
        "latest_posts": latest_posts,
        "other_posts": other_posts,
    }
    return render(request, "blog/index.html", context)

def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    )
    
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "blog/category.html", context)

def blog_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            
            comment = Comment(
                author=request.user,  
                body=form.cleaned_data["body"],
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)

    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        "form": form,
    }

    return render(request, "blog/detail.html", context)


def contact(request):
    template = loader.get_template('contact.html')
    context = {
    'contact' : contact,
  }
    return HttpResponse(template.render(context, request))


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('http://127.0.0.1:8000/login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def dashboard_view(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfileImageForm(instance=user)

    return render(request, 'dashboard.html', {'user': user, 'form': form})

@login_required


@login_required
def upload_profile_image(request):
    if request.method == 'POST':
        print("Request method is POST")
        print("FILES:", request.FILES)  # اینجا را بررسی کنید
        if request.FILES:
            print("FILES received:", request.FILES)
        else:
            print("No FILES received")
        form = ProfileImageForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            print("Form is valid and saved.")
            return redirect('dashboard')  # به صفحه داشبورد هدایت کنید
        else:
            print("Form errors:", form.errors)  # نمایش خطاهای فرم
    else:
        form = ProfileImageForm(instance=request.user)
    return render(request, 'dashboard.html', {'form': form})



class AuthorDetailView(ListView):
    model = Post
    template_name = 'author_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # گرفتن نویسنده بر اساس username از URL
        self.author = get_object_or_404(CustomUser, username=self.kwargs['username'])
        # گرفتن تمام مقالات نوشته شده توسط نویسنده
        return Post.objects.filter(author=self.author)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.author
        return context



class CategoryDetailView(ListView):
    model = Post
    template_name = 'category_detail.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # گرفتن دسته‌بندی بر اساس آی‌دی از URL
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        # گرفتن تمام پست‌های مربوط به این دسته‌بندی
        return Post.objects.filter(categories=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
    



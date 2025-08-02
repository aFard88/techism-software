
from django.http import *
from django.template import loader
from django.contrib.auth import login,authenticate,logout
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .forms import CustomAuthenticationForm


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

def blog_index(request):
    latest_posts = Post.objects.all().order_by('-created_on')[:3]
    other_posts = Post.objects.all().order_by('-created_on')[3:]
    categories = Category.objects.all()
    return render(request, 'main.html', {
        'latest_posts': latest_posts,
        'other_posts': other_posts,
        'categories': categories
    })


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
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        likes_connected = get_object_or_404(Post, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = likes_connected.number_of_likes()
        data['post_is_liked'] = liked
        return data

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
            return redirect('login')
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
        self.author = get_object_or_404(CustomUser, username=self.kwargs['username'])

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

        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        return Post.objects.filter(categories=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
    

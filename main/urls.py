from django.urls import path , re_path
from . import views
from .views import *
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from .forms import CustomAuthenticationForm
from django.contrib.auth import views as auth_views


urlpatterns = [
    #path('', views.main, name='index'),
    path("about/",views.about,name="about"),
    path("dashboard/",views.dashboard , name="dashboard"),
    path('',include("django.contrib.auth.urls")),
    path('register/',views.register,name="register"),
    path("", views.blog_index, name="blog_index"),
    path("post/<int:pk>/", views.blog_detail, name="blog_detail"),
    path("category/<category>/", views.blog_category, name="blog_category"),
    path("contact/",views.contact,name="contact"),
    path('login/', auth_views.LoginView.as_view(authentication_form=CustomAuthenticationForm), name='login'),
    path('upload_profile_image/', upload_profile_image, name='upload_profile_image'),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('author/<str:username>/', AuthorDetailView.as_view(), name='author_posts'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

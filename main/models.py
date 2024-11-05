from django.db import models
from django.contrib.auth.models import User , AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field

class Member(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)

class Category(models.Model):
    name = models.CharField(max_length=30)
    
    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    body = CKEditor5Field('Text', config_name='extends')
    categories = models.ManyToManyField("Category", related_name="posts")
    image = models.ImageField(upload_to='', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , default=1)
    
   
    
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.author} on '{self.post}'"

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(upload_to='', blank=True, null=True)  # فیلد عکس پروفایل
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
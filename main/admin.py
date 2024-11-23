from django.contrib import admin
from main.models import Category, Comment, Post , CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import Post




class CategoryAdmin(admin.ModelAdmin):
    pass


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PostAdminForm, self).__init__(*args, **kwargs)
        self.fields['author'].widget = forms.HiddenInput()  # فیلد author را مخفی می‌کنیم

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'author', 'created_on')

    def save_model(self, request, obj, form, change):
        if not obj.author:  # اگر نویسنده وجود نداشت، نویسنده فعلی را ثبت می‌کنیم
            obj.author = request.user
        obj.save()


class CommentAdmin(admin.ModelAdmin):
    pass



class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'profile_image', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'profile_image')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'profile_image', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
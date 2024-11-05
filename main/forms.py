from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django import forms
from django.contrib.auth.models import User 
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model 
#class CustomUserCreationForm(UserCreationForm):
 #   class Meta(UserCreationForm.Meta):
#        fields = UserCreationForm.Meta.fields + ("email",)

class CommentForm(forms.Form):
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control", 
                "placeholder": "نظر خود را بنویسید...",
                "rows": 4,  # ارتفاع textarea
            }
        )
    )


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "نام کاربری"
        self.fields['email'].label = "ایمیل"
        self.fields['password1'].label = "رمز عبور"
        self.fields['password2'].label = "تکرار رمز عبور"
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        if 'password_based_authentication' in self.fields:
            del self.fields['password_based_authentication']




class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'profile_image')  # فیلدهایی که می‌خواهید نمایش داده شود

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'profile_image')
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="نام کاربری")
    password = forms.CharField(label="رمز عبور")


class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_image'] 



class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label="نام کاربری")
    email = forms.CharField(label="رمز عبور")


from django.contrib.auth.forms import UserCreationForm,UserChangeForm , AuthenticationForm
from django import forms
from django.contrib.auth.models import User 
from .models import CustomUser
from django.contrib.auth import get_user_model 

class CommentForm(forms.Form):
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control", 
                "placeholder": "نظر خود را بنویسید...",
                "rows": 4, 
            }
        )
    )


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "نام کاربری"
        self.fields['email'].label = "ایمیل"
        self.fields['password1']
        self.fields['password2']
        self.fields['username']
        self.fields['password1']
        self.fields['password2']
        if 'password_based_authentication' in self.fields:
            del self.fields['password_based_authentication']





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


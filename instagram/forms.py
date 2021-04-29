
from django.db import models
from django.contrib.auth.forms import UserCreationForm#for signup form
from django.contrib.auth.forms import AuthenticationForm#for login form
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput
from .models import Profile, Comments


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder': 'Username','autocomplete':'off'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))


class UserForm(UserCreationForm):
    email = models.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1','password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder':('Username')})
        self.fields['email'].widget.attrs.update({'placeholder':('Email')})
        self.fields['password1'].widget.attrs.update({'placeholder':('Password')})        
        self.fields['password2'].widget.attrs.update({'placeholder':('Re-enter password')})


        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('fullname',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fullname'].widget.attrs.update({'placeholder':('Fullname')})
       

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)

        self.fields['username'].help_text = None


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('fullname','image', 'bio')
        widgets = {
            'image': forms.FileInput(),
        }

        def __init__(self, *args, **kwargs):
            initial = kwargs.get('initial', {})
            initial['bio'] = self.bio
            kwargs['initial'] = initial
            super(ProfileEditForm, self).__init__(*args, **kwargs)


class CommentForm(forms.ModelForm):
    text = models.TextField(blank = True)

    class Meta:
        model = Comments
        fields = ('text',)
        widgets = {
            'text': forms.TextInput(attrs={
    
                'required': True, 
                'placeholder': 'Add comment ...'
            }),
        }



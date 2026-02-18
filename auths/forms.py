from auths.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Email', 'class':'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password', 'class':'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password', 'class':'form-control'}))

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

class EditProfileForm(forms.ModelForm):
    username = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'Enter Username', 'class':'form-control'}))
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder':'Enter Bio', 'class':'form-control', 'row':3}))
    address = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'Enter Address', 'class':'form-control'}))
    country = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'Enter Country', 'class':'form-control'}))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'bio', 'address', 'country', 'image']

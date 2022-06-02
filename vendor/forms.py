from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class RegistrationForm(UserCreationForm):
    #username = forms.CharField(widget=forms.TextInput(attrs={'class':'w-2/3 h-8 border border-gray-800  pl-2','placeholder':'Username'}))
    #email = forms.EmailField(widget=forms.TextInput(widget=forms.PasswordInput(attrs={'class':'w-2/3 h-8 border border-gray-800  pl-2','placeholder':'Email'})))
    #password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'w-2/3 h-8 border border-gray-800  pl-2','placeholder':'Password'}))
    #password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'w-2/3 h-8 border border-gray-800  pl-2','placeholder':'Confirm password'}))
    class Meta:
        model = User
        fields = ['username','password1','password2','email']


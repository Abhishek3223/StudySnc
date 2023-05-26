from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm


class Room_form(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class myuserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'password1', 'password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'username',  'avatar', 'bio']

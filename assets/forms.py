from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from assets.models import ItemData


# SIGN UP FORM
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Compulsory Field')
    last_name = forms.CharField(max_length=30, required=True, help_text='Compulsory Field')
    email = forms.EmailField(max_length=254, help_text='Required.Enter a valid email address.')
    #   studentID = forms.IntegerField(required=True, help_text='Compulsory Field')
    branch = forms.CharField(max_length=10, required=True, help_text='Compulsory Field')
    #  year = forms.CharField(max_length=10, required=True, help_text='Compulsory Field')
    phone_no = forms.IntegerField(required=True, help_text='Compulsory Field')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


# EDIT PROFILE FORM
class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'email', 'first_name', 'username', 'last_name', 'password')


# REQUEST ITEM FORM
class ItemInfoForm(ModelForm):
    Item_info = forms.CharField(max_length=30, required=True, help_text='Compulsory Field')
    description = forms.CharField(max_length=30, required=True, help_text='Compulsory Field')
    location = forms.CharField(max_length=30, required=True, help_text='Compulsory Field')

    # IMAGE
    # CATEGORY
    # DATE

    class Meta:
        model = ItemData
        fields = ('Item_info', 'description', 'location')

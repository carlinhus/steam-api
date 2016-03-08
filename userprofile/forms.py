from django import forms
from django.contrib.auth.forms import UserCreationForm

class NewUserForm(UserCreationForm):
	steamURL = forms.CharField(label="Steam ID", required=True)
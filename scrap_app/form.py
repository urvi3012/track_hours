from django import forms
from .models import User,Project
from django.contrib.auth.forms import UserCreationForm


class EmployeeUserForm(UserCreationForm):
	first_name = forms.CharField(max_length=200, required=True)
	last_name = forms.CharField(max_length=200, required=True)
	email = forms.EmailField(max_length=254, help_text='Required., in the form abc@xyz.com ')
	is_superuser = forms.BooleanField(initial=False, required=False),
	class Meta:
		model = User
		fields = ('username','first_name', 'last_name', 'email', 'password1', 'password2', 'is_superuser')
		help_texts = {
			'username': None,
			'password':None,
		}

	def save(self, commit = True):
		return super(EmployeeUserForm, self).save(commit=True)

class EmployeeProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		exclude = ('project_working_hrs','project_left_hrs','employee')

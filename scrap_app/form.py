from django import forms
from .models import User,Project
from django.contrib.auth.forms import UserCreationForm


class EmployeeUserForm(UserCreationForm):
	full_name = forms.CharField(max_length=30, required=True, help_text='Optional')
	email = forms.EmailField(max_length=254, help_text='Required., in the form abc@xyz.com ')
	is_superuser = forms.BooleanField(initial=False)
	class Meta:
		model = User
		fields = ('username','full_name', 'email', 'password1', 'password2', 'is_superuser')
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

from django.shortcuts import render,redirect,get_object_or_404
from .models import User,Project
from .form import EmployeeUserForm,EmployeeProjectForm
from django.shortcuts import render
from django.template import loader
from django.views import generic
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from .utils import send_emails,main_function
# from user_addition import add_user
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string
from .serailizer import  ProjectSere
from rest_framework import viewsets
from .pagination import StandardResultsSetPagination

from scrap_app.fetch_data import *

# print("in views", billing_cycles)

class EmployeeRegisterView(generic.CreateView):
	model = User
	form_class = EmployeeUserForm
	template_name = 'employes/emp_register.html'
	success_url = '/user_detail/'


	def form_valid(self,form):
		user = self.request.user
		form.instance.user = user
		return super(EmployeeRegisterView, self).form_valid(form)

class UserDetailView(generic.ListView):
	template_name = 'user/user_detail.html'
	context_object_name = 'user_list'
	queryset = User.objects.all()


class ProjectRegisterView(generic.CreateView):
	model = Project
	form_class = EmployeeProjectForm
	template_name = 'projects/project.html'
	success_url = '/project_detail/'

	def form_valid(self,form):
		if self.request.user.is_superuser:
			form_data=form.save(commit=False)
			form_data.employee=self.request.user
			# form_data.project_working_hrs =form.cleaned_data.get("project_hours")
			form_data.save()
			return super(ProjectRegisterView, self).form_valid(form)
		return redirect('register')	

class ProjectDetailView(generic.ListView):
	template_name = 'projects/project_detail.html'
	context_object_name = 'project_list'
	project_name_list = []
	billing_cycles = []
	developer_name_list = []
	# actual_developer = list(Project.objects.values_list('full_name', flat=True).distinct())
	project_name_list = list(Project.objects.values_list('projects_name', flat=True).distinct())
	project_name_list.sort()
	developer_name_list = list(Project.objects.values_list('developer_name', flat=True).distinct())
	developer_name_list.sort()
	billing_cycles = list(Project.objects.values_list('Month_Cycle', flat=True).distinct())
	billing_cycles.reverse()




	# edit
	actual_developer = list(User.objects.values_list('first_name', 'last_name'))
	for i in range(len(actual_developer)):
		actual_developer[i] = actual_developer[i][0]+" "+actual_developer[i][1]
	actual_developer.sort()

	# edit


	# print(billing_cycles)
	def get_queryset(self):
		if self.request.user.is_superuser:
			if(len(self.billing_cycles) > 0):
				return Project.objects.filter(Month_Cycle = self.billing_cycles[0])
			else:
				return
		else:
			# import pdb; pdb.set_trace()
			return Project.objects.filter(actual_developer = self.request.user.id)

		return Project.objects.filter(pk=self.request.user.id)

	def get_context_data(self, **kwargs):
		context = super(ProjectDetailView, self).get_context_data(**kwargs)
		context['billing_cycles'] = self.billing_cycles
		context['project_name_list'] = self.project_name_list
		context['developer_name_list'] = self.developer_name_list
		context['actual_developer'] = self.actual_developer
		return context


class ProjectApi(viewsets.ModelViewSet):
	serializer_class=ProjectSere
	pagination_class=StandardResultsSetPagination
	def get_queryset(self):
		if self.request.user.is_superuser:
			return Project.objects.all()
		return Project.objects.filter(pk=self.request.user.id)


def drop_down(request):
	billing = ""
	project = ""
	developer = ""
	# actual_developer=""
	if request.method == 'POST':
		billing = request.POST['billing']
		project = request.POST['project']
		developer = request.POST['developer']
		# actual_developer = request.POST['actual_developer']
		
	# print(billing)
	# print(project)
	# print(developer)
	# print(type(project))
	if(project == "0"):
		project = int(project)
	if(developer=="0"):
		developer=int(developer)
	if(billing == "0"):
		billing=int(billing)
	# if (actual_developer == "0"):
	# 	billing = int(actual_developer)
	# import pdb; pdb.set_trace()
	# full_name = actual_developer.first_name + " " + actual_developer.last_name
	# print(full_name)
	if project !=0 and developer !=0 and billing!=0:
		filered_data = Project.objects.filter(Month_Cycle = billing, projects_name = project, developer_name= developer)
	elif project==0 and developer!=0 and billing!=0:
		filered_data = Project.objects.filter(Month_Cycle=billing, developer_name=developer)
	elif developer==0 and			 project!=0 and billing!=0:
		filered_data = Project.objects.filter(Month_Cycle=billing, projects_name=project)
		print(filered_data)
	elif billing==0 and project!=0 and developer!=0:
		filered_data = Project.objects.filter(projects_name=project, developer_name=developer)
	elif project!=0:
		filered_data = Project.objects.filter(projects_name=project)
	elif billing!=0:
		filered_data = Project.objects.filter(Month_Cycle=billing)
		# print(filered_data)
	elif developer!=0:
		filered_data = Project.objects.filter(developer_name=developer)

	# import pdb; pdb.set_trace()
	c = {'project_list': filered_data}
	t = loader.get_template('projects/project_detail_filtered.html')
	html = t.render(c, request)
	t = loader.get_template('projects/_project_detail_filtered.js')
	c = {'html': html}
	return HttpResponse(t.render(c, request), content_type='application/javascript')


# class DeleteObject(generic.DeleteView):
# 	success_url = reverse_lazy('project')
# 	model = Project
#
def Delete_project(request):
	if request.method == 'POST':
		id = request.POST['id']
		# print(id)
		if id:
			# print(id)
			try:
				Project.objects.filter(id=id).delete()
				data = {'status_code': 200, 'status_message': 'Project deleted successfully'}
				messages.success(request, 'Project deleted successfully')
			except Exception as e:
				print(e)
				print ("Not found")
				data = {'status_code': 200, 'status_message': 'Project not found'}
				messages.error(request, 'Project not found')

		else:
			data = {'status_code': 200, 'status_message': 'Project not found'}
			messages.error(request, 'Project not found')
	else:
		data = {'status_code': 400, 'status_message': 'Invalid method'}
	return JsonResponse(data)


class UpdateObject(generic.UpdateView):
	model = Project
	fields = ('actual_developer', 'projects_name', 'project_hours', 'developer_name', 'developer_email')



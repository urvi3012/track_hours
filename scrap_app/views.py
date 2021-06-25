from django.shortcuts import render,redirect,get_object_or_404
from .models import User,Project, Holidays
from .form import EmployeeUserForm,EmployeeProjectForm, UpdateEmpForm, EmployeeUpdateForm
from django.shortcuts import render
from django.template import loader
from django.views import generic
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse,HttpResponseRedirect
from .utils import send_emails
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string
from .serailizer import  ProjectSere
from rest_framework import viewsets
from rest_framework.views import APIView
from .pagination import StandardResultsSetPagination
from django.contrib.auth.mixins import UserPassesTestMixin


from scrap_app.fetch_data import main, get_expected_hours

class Refresh(APIView):
	def get(self, request):
		main()
		return JsonResponse({'success' : True})






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
	queryset = User.objects.filter(is_superuser = 'False').order_by('first_name')


	def get_context_data(self, **kwargs):
		self.actual_developer = User.objects.filter(is_superuser = 'False').order_by('first_name')
		context = super(UserDetailView, self).get_context_data(**kwargs)
		context['actual_developer'] = self.actual_developer
		return context


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
	project_name_list = list(Project.objects.values_list('projects_name', flat=True).distinct())
	project_name_list.sort()
	# print(project_name_list)
	developer_name_list = list(Project.objects.values_list('developer_name', flat=True).distinct())
	developer_name_list.sort()
	billing_cycles = list(Project.objects.values_list('Month_Cycle', flat=True).distinct())
	billing_cycles.reverse()
	actual_developer = User.objects.filter(is_superuser = 'False').order_by('first_name')
	# actual_developer = list(Project.objects.values_list('full_name', flat=True).distinct())

	def get_queryset(self):
		# print("in get qs")
		if self.request.user.is_superuser:
			if(len(self.billing_cycles) > 0):
				return Project.objects.filter(Month_Cycle = self.billing_cycles[0])
			else:
				return
		else:

			return Project.objects.filter(actual_developer = self.request.user.id)

		return Project.objects.filter(pk=self.request.user.id)

	def get_context_data(self, **kwargs):
		self.project_name_list = list(Project.objects.values_list('projects_name', flat=True).distinct())
		self.project_name_list.sort()
		# print(project_name_list)
		self.developer_name_list = list(Project.objects.values_list('developer_name', flat=True).distinct())
		self.developer_name_list.sort()
		self.billing_cycles = list(Project.objects.values_list('Month_Cycle', flat=True).distinct())
		self.billing_cycles.reverse()
		self.actual_developer = User.objects.filter(is_superuser = False).order_by('first_name')
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
	billing = "0"
	project = "0"
	developer = "0"
	ac_dev="0"
	if request.method == 'POST':
		billing = request.POST['billing']
		if(request.POST['project']):
			project = request.POST['project']
		if(request.POST['developer']):
			developer = request.POST['developer']
		if(request.POST['actual_developer']):
			ac_dev = request.POST['actual_developer']


	if(project == "0"):
		project = int(project)
	if(developer=="0"):
		developer=int(developer)
	if(billing == "0"):
		billing=int(billing)
	if(ac_dev == "0"):
		ac_dev=int(ac_dev)

	if project !=0 and developer !=0 and billing!=0 and ac_dev!=0:
		filered_data = Project.objects.filter(Month_Cycle = billing, projects_name = project, developer_name= developer, actual_developer = ac_dev)

	elif project==0 and developer!=0 and billing!=0 and ac_dev!=0 :
		filered_data = Project.objects.filter(Month_Cycle=billing, developer_name=developer, actual_developer = ac_dev)
	elif developer==0 and project!=0 and billing!=0 and ac_dev!=0:
		filered_data = Project.objects.filter(Month_Cycle=billing, projects_name=project, actual_developer = ac_dev)

	elif billing==0 and project!=0 and developer!=0 and ac_dev!=0:
		filered_data = Project.objects.filter(projects_name=project, developer_name=developer, actual_developer = ac_dev)
	elif ac_dev==0 and project!=0 and developer!=0 and billing!=0:
		filered_data = Project.objects.filter(Month_Cycle=billing, projects_name=project, developer_name=developer)

	elif ac_dev == 0 and project == 0 and developer != 0 and billing != 0:
		filered_data = Project.objects.filter(Month_Cycle=billing, developer_name=developer)
	elif ac_dev == 0 and project != 0 and developer == 0 and billing != 0:
		filered_data = Project.objects.filter(Month_Cycle=billing, projects_name=project)
	elif ac_dev == 0 and project != 0 and developer != 0 and billing == 0:
		filered_data = Project.objects.filter( projects_name=project, developer_name=developer)
	elif project == 0 and ac_dev != 0  and developer == 0 and billing != 0:
		filered_data = Project.objects.filter(Month_Cycle=billing, actual_developer = ac_dev)
	elif project == 0 and ac_dev != 0  and developer != 0 and billing == 0:
		filered_data = Project.objects.filter(developer_name=developer, actual_developer = ac_dev)
	elif billing == 0 and ac_dev != 0 and project != 0 and developer == 0:
		filered_data = Project.objects.filter(Month_Cycle=billing, projects_name=project)



	elif project!=0:
		filered_data = Project.objects.filter(projects_name=project)
	elif billing!=0:
		filered_data = Project.objects.filter(Month_Cycle=billing)
	elif developer!=0:
		filered_data = Project.objects.filter(developer_name=developer)
	elif ac_dev!=0:
		filered_data = Project.objects.filter(actual_developer = ac_dev)


	c = {'project_list': filered_data}
	t = loader.get_template('projects/project_detail_filtered.html')
	html = t.render(c, request)
	t = loader.get_template('projects/_project_detail_filtered.js')
	c = {'html': html}
	return HttpResponse(t.render(c, request), content_type='application/javascript')


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


def Delete_employee(request):
	if request.method == 'POST':
		id = request.POST['id']
		# print(id)
		if id:
			# print(id)
			try:
				User.objects.filter(id=id).delete()
				data = {'status_code': 200, 'status_message': 'Employee deleted successfully'}
				messages.success(request, 'Employee deleted successfully')
			except Exception as e:
				print(e)
				print ("Not found")
				data = {'status_code': 200, 'status_message': 'Employee not found'}
				messages.error(request, 'Employee not found')

		else:
			data = {'status_code': 200, 'status_message': 'Employee not found'}
			messages.error(request, 'Employee not found')
	else:
		data = {'status_code': 400, 'status_message': 'Invalid method'}
	return JsonResponse(data)


def Update_project(request, id):
	actual_developer = User.objects.filter(is_superuser=False).order_by('first_name')
	if id:
		try:
			update_pro = Project.objects.get(id=id)
			if request.method == 'POST':
				form = UpdateEmpForm(request.POST, instance = update_pro)
				if form.is_valid():
					# form.save(commit = True)
					post = form.save(commit=False)
					acdev = request.POST['actual_developer']
					print("------ acdev----", acdev)
					post.actual_developer = User.objects.get(id = acdev)
					post.save()
					return redirect('project_detail')
				else:
					print(form.errors)

			return render(request, 'projects/project_update.html', {'update_pro': update_pro, 'id':id, 'actual_developer':actual_developer})

		except Exception as e:
			print(e)
			print ("Not found")
			data = {'status_code': 200, 'status_message': 'Project not found'}
			messages.error(request, 'Project not found')

	else:
		data = {'status_code': 200, 'status_message': 'Project not found'}
		messages.error(request, 'Project not found')

	print("end")
	return JsonResponse(data)


def drop_down_emp(request):
	ac_dev=""

	if request.method == 'POST':
		ac_dev = request.POST['actual_developer']

	if (ac_dev == "0"):
		filered_data = User.objects.all()
	elif ac_dev != "0":
		filered_data = User.objects.filter(id = ac_dev)

	print(filered_data)

	c = {'user_list': filered_data}
	t = loader.get_template('user/emp_detail_filtered.html')
	html = t.render(c, request)
	t = loader.get_template('user/_emp_detail_filtered.js')
	c = {'html': html}
	return HttpResponse(t.render(c, request), content_type='application/javascript')


def Update_user(request, id):
	if id:
		try:
			update_user = User.objects.get(id=id)
			if request.method == 'POST':
				form = EmployeeUpdateForm(request.POST, instance = update_user)
				if form.is_valid():
					form.save(commit = True)

					return redirect('user_detail')
				else:
					print(form.errors)

			return render(request, 'user/user_update.html', {'update_user': update_user, 'id':id})

		except Exception as e:
			print(e)
			print ("Not found")
			data = {'status_code': 200, 'status_message': 'User not found'}
			messages.error(request, 'User not found')

	else:
		data = {'status_code': 200, 'status_message': 'User not found'}
		messages.error(request, 'User not found')
	return JsonResponse(data)


def Update_user_form(request):
	data = {'status_code': 200, 'status_message': 'user not found'}
	if request.method == 'POST':
		user_id = request.POST['user_id']
		user_user_name = request.POST['user_user_name']
		developer_first_name = request.POST['developer_first_name']
		developer_last_name = request.POST['developer_last_name']
		developer_email = request.POST['developer_email']
		is_super = request.POST.get('is_superuser', False)
		if user_id:
			try:
				user = User.objects.get(username=user_user_name)

			except:
				user = None
				data = {'status_code': 200, 'status_message': 'user not found'}

			if user and user.id != int(user_id):

				data = {'status_code': 200, 'status_message': 'User name already exist, please select other username'}
				messages.error(request, 'Username exist')
			else:
				try:
					user = User.objects.get(id=user_id)
					user.username = user_user_name
					user.first_name = developer_first_name
					user.last_name = developer_last_name
					user.email = developer_email
					user.is_superuser = is_super
					user.save()
					data = {'status_code': 200, 'status_message': 'User updated'}
					return HttpResponseRedirect('/user_detail/')
				except:
					user = None
					data = {'status_code': 200, 'status_message': 'User not found'}

	return JsonResponse(data)


import datetime

def Save_Holidays(request):
	# import pdb; pdb.set_trace()
	if request.method == 'POST':
		dates = request.POST['dates']
	dates= dates.split(',')
	print(dates)
	for i in dates:
		i = datetime.datetime.strptime(i, "%d-%m-%Y").strftime("%Y-%m-%d")
		if not Holidays.objects.filter(holidays=i).exists():
			holiday_obj = Holidays.objects.create(holidays=i)
			holiday_obj.save()
	get_expected_hours()

	return redirect('project_detail')


from django.urls import path
from scrap_app import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import user_passes_test

# app_name = 'scrap_app'

project = views.ProjectApi.as_view({'get': 'list'})

urlpatterns =[
	path('',auth_views.LoginView.as_view(template_name = "employes/login.html"), name="login"),
	path('logout/',auth_views.LogoutView.as_view(next_page='login'),name="logout"),
	path('register/',views.EmployeeRegisterView.as_view(),name='register'),
	path('project/',views.ProjectRegisterView.as_view(),name='project'),
	# path('employee_project_detail/',views.UserProjectDetailView.as_view(),name='user_project_detail'),
	path('project_detail/',views.ProjectDetailView.as_view(),name='project_detail'),
	path('user_detail/',views.UserDetailView.as_view(),name='user_detail'),
	path('projectlist/',project),
	path('dropdown/',views.drop_down, name='drop_down'),
	# path('dropdown_u/',views.drop_down_user, name='drop_down_user'),
	path('dropdown-emp/', views.drop_down_emp, name='drop_down_emp'),
	path('deleteproject/',views.Delete_project, name='delete'),
	path('updateproject/<id>', views.Update_project, name='update'),
	path('updateuser/<id>', views.Update_user, name='update-user'),
	path('updateuserform/', views.Update_user_form, name='update-user-form'),
	path('project_detail_refresh/', views.Refresh.as_view(), name='refresh'),
	path('deleteemployee/',views.Delete_employee, name='delete-emp'),

]
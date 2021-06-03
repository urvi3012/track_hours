from django.urls import path
from scrap_app import views
from django.contrib.auth import views as auth_views

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
	path('delete/<pk>/',views.DeleteObject.as_view(), name='delete'),
	path('update/<pk>/',views.UpdateObject.as_view(), name='update'),
	# path('dropdowndev/', views.drop_down_dev, name='drop_down_dev'),
	# path('dropdownpro/', views.drop_down_pro, name='drop_down_pro'),


]
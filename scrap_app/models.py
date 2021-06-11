from django.db import models
# from django.contrib.gis.db import models
from django.contrib.auth.models import User

from django.urls import reverse


class Project(models.Model):
	actual_developer = models.ForeignKey(User,null = True,blank=True, on_delete=models.CASCADE)
	# actual_developer = models.CharField(User,null = True,blank=True, max_length=200)
	projects_name = models.CharField(max_length=100)
	project_hours = models.CharField(max_length=100)
	developer_name = models.CharField(max_length=255)
	Month_Cycle = models.CharField(max_length = 1000, blank=True, null=True)
	project_working_hrs = models.CharField(max_length=50,null=True,blank=True)
	project_left_hrs = models.CharField(max_length=50,default="8 Hr 00 Min",null=True,blank=True)
	mailing_hrs = models.CharField(max_length=100,null=True,blank=True)
	developer_email = models.EmailField()

	def get_absolute_url(self):
		return reverse('project')

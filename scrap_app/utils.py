import sys
from django.conf import settings
from .models import *
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string
import re

def get_time(t):
    a = re.split(' ', t)
    if (len(a) == 6):
        a = [int(a[0]), int(a[2]), int(a[4])]
    elif (len(a) == 4):
        a = [int(a[0]), int(a[2]), 0]
    elif (len(a) == 2):
        a = [int(a[0]), 0, 0]
    else:
        a = [0, 0, 0]
    return a

def convert(seconds):
    print(seconds)
    a=str(seconds//3600)
    b=str((seconds%3600)//60)
    c=str((seconds%3600)%60)
    return a,b,c



def check_hours(i):
    ex_daily_hours = []
    t = i.project_hours
    e = i.expected_daily_hours
    t = get_time(t)
    e = get_time(e)
    total_sec_e = (e[0] * 60 * 60) + (e[1] * 60) + e[2]
    total_sec_t = (t[0] * 60 * 60) + (t[1] * 60) + t[2]
    if(total_sec_t < total_sec_e):
        ex_daily_hours[0], ex_daily_hours[1], ex_daily_hours[2] = convert(total_sec_e-total_sec_t)
        msg = f'{ex_daily_hours[0]} Hrs {ex_daily_hours[1]} Mins {ex_daily_hours[2]} Sec'
        return msg
    else:
        return 0


def send_emails(user_name,email,project_name):
    hours = Project.object.all()
    for i in hours:
        msg = check_hours(i)
        if msg != 0:
            subject= 'Email Confirmation '
            from_email = settings.DEFAULT_EMAIL_FROM
            html_message = render_to_string('send_mails.html', {'object': user_name , 'msg' : msg , 'current_project':project_name})
            msg = EmailMultiAlternatives(subject, html_message, from_email,[email])
            msg.attach_alternative(html_message, "text/html")
            msg.send()
            print('mail sent')
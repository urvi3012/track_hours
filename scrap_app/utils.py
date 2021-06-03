import sys
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string

hrs=0
mins=0

def convert(time_input):
    hrs=0
    mins=0
    if("Hr" in time_input and "M" in time_input ):
        sn=2
        groups = time_input.split(' ')
        groups=' '.join(groups[:sn]), ' '.join(groups[sn:])
        hrs=groups[0].split(' H')[0]
        if("M" in time_input ):
            mins=groups[1].split(' M')[0]
        
    elif("Hr" in time_input and "M" not in time_input ):
        groups = time_input.split(' Hr')
        hrs=groups[0]
        mins=0

    elif("Hr" not in time_input and "M" in time_input):
        if("M" in time_input):
            groups = time_input.split(' M')
        mins=groups[0]
        hrs=0
    
    hrs=int(hrs)
    mins=int(mins)
    
    return hrs, mins
    
def return_hours(in_hrs, in_mins, minus_hrs, minus_mins, addition):
    total_time_in = (in_hrs*60) + in_mins
    total_time_minus = (minus_hrs*60) + minus_mins
    #print(total_time_in, total_time_minus)
    if(addition == 0):
        if(total_time_in >= total_time_minus):
            time_left = total_time_in - total_time_minus
            minutes_left = time_left % 60
            # Get hours with floor division
            hours_left_h = time_left // 60
            return hours_left_h, minutes_left

        else:
            hrs=0
            mins=0
            return hrs, mins
    else:
        time_left = total_time_in + total_time_minus
        minutes_left = time_left % 60
        # Get hours with floor division
        hours_left_h = time_left // 60
        return hours_left_h, minutes_left



def main_function(time_input,time_left, addition):
    if(addition==1):    
        if(time_input == '0'):
            minus_hrs, minus_mins = convert(time_input)
            ans =  str(minus_hrs) + " Hr " + str(minus_mins) + " Min"
            return ans
        
        elif(time_left == '0'):
            minus_hrs, minus_mins = convert(time_left)
            ans = str(minus_hrs) + " Hr " + str(minus_mins) + " Min"
            return ans
        
        else:
            in_hrs,  in_mins = convert(time_input)
            to_minus_hrs, to_minus_mins = convert(time_left)
            minus_hrs, minus_mins =  return_hours(in_hrs, in_mins, to_minus_hrs, to_minus_mins, addition)
            ans = str(minus_hrs) + " Hr " + str(minus_mins) + " Min"
            return ans
    else:
        if(time_input == '0'):
            minus_hrs, minus_mins = convert(time_left)
            ans =  str(minus_hrs) + " Hr " + str(minus_mins) + " Min"
            return ans
        
        elif(time_left == '0'):
            minus_hrs, minus_mins = convert(time_input)
            ans = str(minus_hrs) + " Hr " + str(minus_mins) + " Min"
            return ans
        
        else:
            in_hrs,  in_mins = convert(time_input)
            to_minus_hrs, to_minus_mins = convert(time_left)
            minus_hrs, minus_mins =  return_hours(in_hrs, in_mins, to_minus_hrs, to_minus_mins, addition)
            ans = str(minus_hrs) + " Hr " + str(minus_mins) + " Min"
            return ans
    

def send_emails(user_name,pending_hrs,email,project_name):
    subject= 'Email Confirmation '
    from_email = settings.DEFAULT_EMAIL_FROM
    html_message = render_to_string('send_mails.html', {'object': user_name , 'pending_hrs' : pending_hrs , 'current_project':project_name})
    msg = EmailMultiAlternatives(subject, html_message, from_email,[email])
    msg.attach_alternative(html_message, "text/html")
    msg.send()
    print('mail sent')
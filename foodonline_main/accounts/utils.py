from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings


# for detecting the user in myaccounts url and views
def detectUser(user):
    if user.role==1:
        redirectUrl='vendorDashboard'
        return redirectUrl
    elif user.role==2:
        redirectUrl='customerDashboard'
        return redirectUrl      
    elif user.role == None and user.is_superadmin:
        redirectUrl='/admin'
        return redirectUrl  


# send verification email
def send_verification_email(request, user, mail_subject, mail_template):
    from_email = settings.DEFAULT_FROM_EMAIL #from email is ooptional
    current_site = get_current_site(request)
    message = render_to_string(mail_template, {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)), # user ki id ko direct nai bhjskte encode krna prega
        'token': default_token_generator.make_token(user),  #user k liye token banaega
    })
    to_email=user.email
    mail = EmailMessage(mail_subject,message,from_email,to=[to_email])
    mail.send()

    

    
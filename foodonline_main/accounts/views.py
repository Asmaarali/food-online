from django.shortcuts import render, redirect
from django.http import HttpResponse

from vendor.forms import VendorForm
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import (
    messages,
    auth,
)  # if we use this then views name can be login or logout and call it using auth.login() auth.logout auth.authenticate

from django.contrib.auth import (
    authenticate,
    login,
    logout,
)  # if we use this library then veiws name donot be login or logout and call it with auth
from .utils import detectUser, send_verification_email 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import (
    PermissionDenied,
)  # custom decorators ,, permission denied is a http error 403...to create the page just name 403.html

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from vendor.models import Vendor


#!Custom decorators
# restrict the customer to accessing the vendor dashboard from url
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


# restrict the vendor to accessing the customer dashboard from url
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# Create your views here.


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already login")
        return redirect("myAccount")

    form = UserForm()
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            # created user using form
            user = form.save(commit=False)
            user.role = User.CUSTOMER
            password = form.cleaned_data["password"]
            user.set_password(password)
            user.save()

            # send verification email
            mail_subject = 'Plz acivate your account'
            mail_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, mail_template)

            messages.success(request, "Verification link has sent to your email address!")
            return redirect("registerUser")

            # aalso create user using method create_user in models
            # first_name=form.cleaned_data['first_name']
            # last_name=form.cleaned_data['last_name']
            # email=form.cleaned_data['email']
            # username=form.cleaned_data['username']
            # password=form.cleaned_data['password']
            # user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            # user.role=2
            # user.save()
            # return redirect('registerUser')

    context = {"form": form}
    return render(request, "accounts/registerUser.html", context)


def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already login")
        return redirect("myAccount")

    form = UserForm()
    v_form = VendorForm()
    if request.method == "POST":
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
            )
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            # print(f"user = {user}")
            # print(f"user_prrofile = {user_profile}")
            vendor.user_profile = user_profile
            vendor.save()

            # send verification email
            mail_subject = 'Plz acivate your account'
            mail_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, mail_template)

            messages.success(
                request,
                "verification link has sent to your email address , please wait for the approval!",
            )
            return redirect("registerVendor")
    context = {
        "form": form,
        "v_form": v_form,
    }
    return render(request, "accounts/registerVendor.html", context)


def activate(request, uidb64, token):
    # Activating the user by is_active status True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,"Account activated successfully!!")
        return redirect('login')
    else:
        messages.error(request,"Invalid verification link !!")
        return redirect('login')


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already login")
        return redirect("myAccount")
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(email=email, password=password)
        # print(user)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "Login successfully")
            return redirect("myAccount")
        else:
            messages.error(request, "invalid credential")
            print("error")
    return render(request, "accounts/login.html")


def handlelogout(request):
    auth.logout(request)
    messages.success(request, "Logout successfull")
    return redirect("login")


@login_required(login_url="login")
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)


@login_required(login_url="login")
@user_passes_test(check_role_customer)
def customerDashboard(request):
    return render(request, "accounts/customerDashboard.html")


@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, "accounts/vendorDashboard.html")


# Reset password work
def forgot_password(request):
    if request.method == 'POST':
        email=request.POST['email'].lower()
        if User.objects.filter(email__exact=email).exists():
            user = User.objects.get(email__exact=email)
            
            # send verification email
            mail_subject = 'Reset your password'
            mail_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject, mail_template)
            
            messages.success(request, "Reset password link has send to your email")            
            return redirect('forgot_password')
        else:
            messages.error(request, "Email doesnot exists")
            return redirect('forgot_password')
            
        
    return render(request,"accounts/forgot_password.html")

def reset_password_validate(request, uidb64, token):
    # Activating the user by is_active status True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.info(request, "Reset your password")
        return redirect('reset_password') 
    else:
        messages.error(request,"Invalid verification link !!")
        return redirect('login')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            pk = request.session.get('uid')
            print(pk)
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, "Password has been changed successfully")
            return redirect('login') 
        else:
            messages.error(request,"Password didnot match !!")
            return redirect('reset_password')            
    return render(request,"accounts/reset_password.html")

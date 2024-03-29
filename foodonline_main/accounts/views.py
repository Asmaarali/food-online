from django.shortcuts import render , redirect
from django.http import HttpResponse

from vendor.forms import VendorForm
from .forms import UserForm 
from .models import User , UserProfile
from django.contrib import messages , auth # if we use this then views name can be login or logout and call it using auth.login() auth.logout auth.authenticate

from django.contrib.auth import authenticate , login , logout     #if we use this library then veiws name donot be login or logout and call it with auth
from .utils import detectUser
from django.contrib.auth.decorators import login_required , user_passes_test
from django.core.exceptions import PermissionDenied #custom decorators
#!Custom decorators
# restrict the customer to accessing the vendor dashboard from url
def check_role_customer(user):
    if user.role==2:
        return True
    else:
        raise PermissionDenied
# restrict the vendor to accessing the customer dashboard from url
def check_role_vendor(user):
    if user.role==1:
        return True
    else:
        raise PermissionDenied
    

# Create your views here.

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already login')
        return redirect('myAccount')
    
    
    form=UserForm()
    if request.method=="POST":
        form=UserForm(request.POST)
        if form.is_valid():
            # created user using form
            user=form.save(commit=False)
            user.role=User.CUSTOMER
            password=form.cleaned_data['password']
            user.set_password(password)
            user.save()
            messages.success(request,'User has been registered succesfully!')
            return redirect('registerUser')

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
        
    context={
        'form':form
    }
    return render(request,"accounts/registerUser.html",context)

def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already login')
        return redirect('myAccount')

    form=UserForm()
    v_form=VendorForm()
    if request.method == "POST":
        form=UserForm(request.POST)
        v_form=VendorForm(request.POST,request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role=User.VENDOR
            user.save()
            vendor=v_form.save(commit=False)
            vendor.user=user
            user_profile=UserProfile.objects.get(user=user)
            vendor.user_profile=user_profile
            vendor.save()
            messages.success(request,'Vendor has been registered succesfully , please wait for the approval!')
            return redirect('registerVendor')
    context={
        'form': form,
        'v_form':v_form,
    }
    return render(request,"accounts/registerVendor.html",context)


def login(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already login')
        return redirect('myAccount')
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(email=email,password=password)
        # print(user)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'Login successfully')
            return redirect('myAccount')
        else:
            messages.error(request, "invalid credential")
            print("wrror")
    return render(request,"accounts/login.html")


def handlelogout(request):
    auth.logout(request)
    messages.success(request,'Logout successfull')
    return redirect('login')

@login_required(login_url='login')
def myAccount(request):
    user=request.user
    redirectUrl=detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerDashboard(request):
    return render(request,"accounts/customerDashboard.html")

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request,"accounts/vendorDashboard.html")

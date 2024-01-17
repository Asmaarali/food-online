from django.shortcuts import render , redirect
from django.http import HttpResponse

from vendor.forms import VendorForm
from .forms import UserForm 
from .models import User , UserProfile
from django.contrib import messages
# Create your views here.

def registerUser(request):
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
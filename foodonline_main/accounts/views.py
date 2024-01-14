from django.shortcuts import render , redirect
from django.http import HttpResponse
from .forms import UserForm 
from .models import User
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
            messages.success(request,'User has been registered succesfully')
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
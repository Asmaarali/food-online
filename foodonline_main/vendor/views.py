from django.shortcuts import render , get_object_or_404 , redirect
from .forms import VendorForm 
from accounts.forms import UserProfileForm

from accounts.models import UserProfile
from .models import Vendor

from django.contrib import messages

# Create your views here.
def vprofile(request):
    print(request.user)
    profile = get_object_or_404(UserProfile , user=request.user) #user is a field name
    vendor = get_object_or_404(Vendor , user=request.user)
    profile_form = UserProfileForm(instance=profile)
    vendor_form = VendorForm(instance=vendor)
    # print(profile)
    # saving form
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST,request.FILES,instance=profile)
        vendor_form = VendorForm(request.POST,request.FILES,instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request,"Profile updated successfully!")
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)

    
    context={
        'profile_form':profile_form,
        'vendor_form':vendor_form,
        'profile':profile,
        'vendor':vendor,
    }
    
    return render(request,"vendor/vprofile.html" ,context)
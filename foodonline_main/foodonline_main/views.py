from django.shortcuts import render,redirect
from vendor.models import Vendor

def index(request):
    vendors = Vendor.objects.filter(is_approved=True , user__is_active=True)[:8]
    # print(vendors)
    context={
        'vendors':vendors
    }
    return render(request,"index.html",context)
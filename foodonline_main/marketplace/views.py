from django.shortcuts import render
from menu.models import Category , FoodItem
from vendor.models import Vendor
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch

# Create your views here.

def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True , user__is_active=True)
    context={
        'vendors':vendors
    }
    return render(request,"marketplace/listing.html", context)

def vendor_detail(request , vendor_slug):
    vendor = get_object_or_404(Vendor , vendor_slug=vendor_slug)
    # print(vendor)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset= FoodItem.objects.filter(is_available=True)
        )
    )

    context={
        'vendor':vendor,
        'categories':categories,
    }
    return render(request,"marketplace/vendor_detail.html",context)
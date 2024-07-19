from django.shortcuts import render , get_object_or_404 , redirect
from .forms import VendorForm , OpeningHourForm
from accounts.forms import UserProfileForm

from accounts.models import UserProfile
from .models import Vendor , OpeningHour

from django.contrib import messages

from menu.models import Category ,  FoodItem

from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor

from menu.forms import CategoryForm , FoodItemForm
from django.template.defaultfilters import slugify

from django.http import HttpResponse , JsonResponse
from django.db import IntegrityError

# Helper function
def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor

# Create your views here.
@login_required(login_url="login")
@user_passes_test(check_role_vendor)
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

@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    # print(vendor)
    categories = Category.objects.filter(vendor=vendor)
    
    context={
        'categories':categories,
        
    }
    return render(request,"vendor/menu_builder.html", context)


@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def fooditems_by_category(request , pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category , pk=pk)  #getting category by pk
    # print(category)
    fooditems = FoodItem.objects.filter(vendor=vendor , category=category)
    # print(fooditems)
    context={
        'fooditems':fooditems,
        'category':category,
    }
    
    return render(request,"vendor/fooditems_by_category.html",context)


# category crud 

@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def add_category(request):
    form = CategoryForm()
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category_name = form.cleaned_data['category_name']
            category.slug = slugify(category_name)
            form.save()
            messages.success(request,"Added succesfully!")
            return redirect('menu_builder')
    context = {
        'form':form
    }
    return render(request,"vendor/add_category.html",context)

@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def edit_category(request , pk=None):
    category = get_object_or_404(Category ,pk=pk)
    form = CategoryForm(instance=category)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST ,instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category_name = form.cleaned_data['category_name']
            category.slug = slugify(category_name)
            form.save()
            messages.success(request,"Updated succesfully!")
            return redirect('menu_builder')
    context = {
        'form':form,
        'category':category
    }
    return render(request,"vendor/edit_category.html",context)

@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def delete_category(request , pk=None):
    category = get_object_or_404(Category ,pk=pk)
    category.delete()
    messages.success(request,"Category deleted succesfully!")
    return redirect('menu_builder')

# food crud

@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def add_food(request):
    form = FoodItemForm()
    #modify category to show only category own particular vendor
    form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    if request.method == 'POST':
        form = FoodItemForm(request.POST , request.FILES)
        if form.is_valid():
            food=form.save(commit=False)
            food.vendor = get_vendor(request)
            food_title=form.cleaned_data['food_title']
            food.slug = slugify(food_title)
            form.save()
            messages.success(request,"Food added succesfully!")
            return redirect('fooditems_by_category', food.category.id)
        
    context = {
        'form': form
    }
    return render(request,"vendor/add_food.html",context)

@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def edit_food(request , pk=None):
    food = FoodItem.objects.get(id=pk)
    form = FoodItemForm(instance=food)
    form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    if request.method == 'POST':
        form = FoodItemForm(request.POST , request.FILES , instance=food)
        if form.is_valid():
            food=form.save(commit=False)
            food.vendor = get_vendor(request)
            food_title=form.cleaned_data['food_title']
            food.slug = slugify(food_title)
            form.save()
            messages.success(request,"Updated succesfully!")
            return redirect('fooditems_by_category', food.category.id)
    context={
        'form':form,
        'food':food
    }
    return render(request,"vendor/edit_food.html",context)
    

@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def delete_food(request , pk=None):
    food = get_object_or_404(FoodItem ,pk=pk)
    food.delete()
    messages.success(request,"Food deleted succesfully!")
    return redirect('menu_builder')


def opening_hours(request):
    vendor_opening_hour = OpeningHour.objects.filter(vendor = get_vendor(request))
    # print(vendor_opening_hour)
    form = OpeningHourForm()
    context = {
        'form':form,
        'vendor_opening_hour':vendor_opening_hour
    }
    
    return render(request , "vendor/opening_hours.html" , context)


def add_opening_hours(request):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
            # test = request.POST.get('test')
            # print(test)
            day = request.POST.get('day')
            from_hour = request.POST.get('from_hour')
            to_hour = request.POST.get('to_hour')
            is_closed = request.POST.get('is_closed')
            
            try:
                created = OpeningHour.objects.create(vendor=get_vendor(request),day=day,from_hour=from_hour,to_hour=to_hour,is_closed=is_closed)
                if created:
                    oh = OpeningHour.objects.get(id = created.id)
                    if oh.is_closed:
                        return JsonResponse({'status':'success','day':oh.get_day_display(),'is_closed':'Closed','id':oh.id})
                    else:
                        return JsonResponse({'status':'success','day':oh.get_day_display(),'from_hour':oh.from_hour,'to_hour':oh.to_hour,'id':oh.id})
            except IntegrityError as e:
                return JsonResponse({'status':'failed','message':from_hour + ' to ' + to_hour + ' already exists for this day' })
        else:
            HttpResponse('invalid response')
            
    return HttpResponse('add opening hour asmoo')


def remove_opening_hours(request , pk=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            oh = get_object_or_404(OpeningHour,id=pk)
            oh.delete()
            return JsonResponse({'status':'success','id':pk})
from django.shortcuts import render , get_object_or_404 , redirect
from .forms import VendorForm 
from accounts.forms import UserProfileForm

from accounts.models import UserProfile
from .models import Vendor

from django.contrib import messages

from menu.models import Category ,  FoodItem

from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor

from menu.forms import CategoryForm , FoodItemForm
from django.template.defaultfilters import slugify

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
from django.http import HttpResponse , JsonResponse
from django.shortcuts import render , redirect
from menu.models import Category , FoodItem
from vendor.models import Vendor , OpeningHour
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from .models import Cart
from .context_processors import get_cart_counter , get_cart_amount
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import date , datetime
from django.db.models import Q


# Create your views here.

def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True , user__is_active=True)
    context={
        'vendors':vendors
    }
    return render(request,"marketplace/listing.html", context)




def vendor_detail(request , vendor_slug):
    vendor = get_object_or_404(Vendor , vendor_slug=vendor_slug)
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    
    # print(q)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset= FoodItem.objects.filter(category__category_name__icontains = q ,is_available=True)
        )
    )
    cat = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset= FoodItem.objects.filter(is_available=True)
        )
    )
    # for cat in categories:
    #     print(f'{cat} , {cat.fooditems.all()}')
    
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None

    
    # opening hours
    opening_hours = OpeningHour.objects.filter(vendor = vendor).order_by('day','-from_hour')
    # check current opening hours
    c_today = date.today()
    today = c_today.isoweekday()
    # print(c_today)
    current_opening_hours = OpeningHour.objects.filter(vendor=vendor , day = today)
    # print(opening_hours)
        
    context={
        'q':q,
        'cat':cat,
        'vendor':vendor,
        'categories':categories,
        'cart_items':cart_items,
        'opening_hours':opening_hours,
        'current_opening_hours':current_opening_hours,
    }
    return render(request,"marketplace/vendor_detail.html",context)

# add to cart
def add_to_cart(request , food_id):
    if request.user.is_authenticated:
        # check if only ajax request
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # check if the food item exits
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # check if the user has already added the food to the cart
                try:
                    chkCart=Cart.objects.get(user=request.user, fooditem=fooditem)
                    # increase the cart
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': 'success','message':'Cart increased','cart_counter': get_cart_counter(request) , 'qty':chkCart.quantity , 'cart_amount': get_cart_amount(request)})
                except:
                    # create cart if food not added
                    chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'success','message':'Added the food to the cart','cart_counter': get_cart_counter(request) , 'qty':chkCart.quantity , 'cart_amount': get_cart_amount(request)})
            except:
                return JsonResponse({'status': 'failed','message':'Food doesnot exist!'})
        else:
            return JsonResponse({'status': 'failed','message':'Invalid request'})
    else:
        return JsonResponse({'status': 'login_required','message':'you are not loggedin'})
    
# decrease cart
def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        # check if only ajax request
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # check if the food item exits
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # check if the user has already added the food to the cart
                try:
                    chkCart=Cart.objects.get(user=request.user, fooditem=fooditem)
                    # Decrease the cart
                    if chkCart.quantity > 1:
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                    return JsonResponse({'status': 'success','cart_counter': get_cart_counter(request) , 'qty':chkCart.quantity , 'cart_amount': get_cart_amount(request)})
                except:
                    return JsonResponse({'status': 'failed','message':'You donot have this item in your cart'})
            except:
                return JsonResponse({'status': 'failed','message':'Food doesnot exist!'})
        else:
            return JsonResponse({'status': 'failed','message':'Invalid request'})
    else:
        return JsonResponse({'status': 'login_required','message':'you are not loggin'})


# cart page
@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by("created_at")

    context = {
        'cart_items': cart_items,
    }
    return render(request,"marketplace/cart.html", context)


# delete cart item in cart page
def delete_cart(request , cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                cart_item = Cart.objects.get(user=request.user,id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'success','message':'Cartitem has been deleted!','cart_counter': get_cart_counter(request) , 'cart_amount': get_cart_amount(request)})
                    
            except:
                return JsonResponse({'status': 'failed','message':'Cartitem doesnot exist!'})
        else:
            return JsonResponse({'status': 'failed','message':'Invalid request'})
    else:
        return JsonResponse({'status': 'login_required','message':'you are not loggin'})
    

def search(request):
    get_search = request.GET['search']
    
    if not get_search:
        return render(request, "marketplace/listing.html", {'vendors': Vendor.objects.none()})

    # get vendor ids that has the food item the user is looking for 
    fetch_all_vendor_ids_by_foodname = FoodItem.objects.filter(food_title__icontains = get_search , is_available = True).values_list('vendor' , flat=True)
    # print(fetch_all_vendor_ids_by_foodname) 
    
    vendors = Vendor.objects.filter(Q(pk__in=fetch_all_vendor_ids_by_foodname) | Q(vendor_name__icontains = get_search , is_approved = True , user__is_active = True))
    
    context = {
        'vendors': vendors
    }
    return render(request,"marketplace/listing.html", context)


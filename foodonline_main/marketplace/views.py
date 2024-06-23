from django.http import HttpResponse , JsonResponse
from django.shortcuts import render , redirect
from menu.models import Category , FoodItem
from vendor.models import Vendor
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from .models import Cart
from .context_processors import get_cart_counter , get_cart_amount
from django.contrib.auth.decorators import login_required

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
    # for cat in categories:
    #     print(f'{cat} , {cat.fooditems.all()}')
    
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None

    context={
        'vendor':vendor,
        'categories':categories,
        'cart_items':cart_items,
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
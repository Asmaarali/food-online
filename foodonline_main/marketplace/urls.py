from django.urls import path
from . import views


urlpatterns = [
    path("", views.marketplace, name="marketplace"),

    
    # add to cart
    path("add_to_cart/<int:food_id>/", views.add_to_cart, name="add_to_cart"),
    # decrease cart
    path("decrease_cart/<int:food_id>/", views.decrease_cart, name="decrease_cart"),
    # cart page
    path("cart/",views.cart,name="cart"), # if cartpage is raising error by vendor_detail because slug not matches it is thinking like its a slug so put vendor _detail path after cart path then it quickfix

    # delete cart item in cart page
    path("delete/<int:cart_id>/",views.delete_cart,name="delete_cart"),
    
    # searching
    path("search",views.search,name="search"),
    
    # put after because cart and search raising error that it thinks its a slug so put after this and its work
    path("<slug:vendor_slug>", views.vendor_detail, name="vendor_detail"),
]

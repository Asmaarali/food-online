from django.urls import path
from . import views

urlpatterns=[
    path('registerUser/',views.registerUser,name='registerUser'),
    path('registerVendor/',views.registerVendor,name='registerVendor'),

    path('login/',views.login,name='login'),
    path('logout/',views.handlelogout,name='handlelogout'),
    path('myAccount/',views.myAccount,name='myAccount'),  # function for detecting user dashboard
    path('customerDashboard/',views.customerDashboard,name='customerDashboard'),
    path('vendorDashboard/',views.vendorDashboard,name='vendorDashboard'),
    
]
from django.urls import path , include
from . import views

urlpatterns=[
    path("", views.myAccount),
    
    path('registerUser/',views.registerUser,name='registerUser'),
    path('registerVendor/',views.registerVendor,name='registerVendor'),

    path('login/',views.login,name='login'),
    path('logout/',views.handlelogout,name='handlelogout'),
    path('myAccount/',views.myAccount,name='myAccount'),  # function for detecting user dashboard
    path('customerDashboard/',views.customerDashboard,name='customerDashboard'),
    path('vendorDashboard/',views.vendorDashboard,name='vendorDashboard'),

    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/',views.reset_password_validate,name='reset_password_validate'),
    path('reset_password/',views.reset_password,name='reset_password'),
    
    path('vendor/',include('vendor.urls')),
    
    # check email & username exist using ajax
    path('check_user_exists/',views.check_user_exists,name="check_user_exists"),
    path('check_username_exists/',views.check_username_exists,name="check_username_exists"),
]
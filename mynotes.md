<!-- !------------------------foodonline advanced notes-------------------------------- -->
<!-- *important packages: -->
1) for postgres database setup install psycopj2 package
2) for securing password and sensitive information befor handover the project to someone install python-decouple package...and create .env file in main root folder then store there in key value pair and call it to setting using config('demo')
3) cretae .gitignore file in root directory to exclude unnecessory files to push on github...goto gitignore.io and type django and paste all the stuff in .gitignorefile













<!-- !Notes -->
1) Abstractuser extends the user class and add your features or additional fields
2) Abstractbaseuser  Use this option if you want to start from scratch by creating your own, completely new user model.
3) Baseusermanager BaseUserManager is a class provided by Django that includes methods for creating User instances. it has two methods one for regular user and another one for superuser..its has no fields it only describe the way for actual user and superuser

4) null=True,Black=True:
In Django models, blank=True and null=True serve different purposes:

blank=True: This parameter applies to form validation. When blank=True is set for a field, it means that the field is not required in forms. It allows the field to be left empty when submitting forms. This doesn’t affect the database schema directly but impacts form validation.

null=True: This parameter applies to the database schema. When null=True is set for a field, it means that the field in the database can hold a NULL value. If null=True is not specified and a field is left empty, Django will store an empty string ('') instead of a NULL in the database for fields like CharField or TextField.

For example, with blank=True and null=True on the phone_number field:

phone_number = models.CharField(max_length=12, blank=True, null=True)

If you save an instance without a value for phone_number, the field can be empty in the form (blank=True), and in the database, it can be NULL (null=True). This means that in the database, the field for that record will contain a NULL value instead of an empty string.
So, if you have a record with an empty phone number, and null=True is set, in the database it will be represented as NULL rather than an empty string, differentiating it from a scenario where the field doesn’t accept NULL values.

5) from django.contrib.auth.admin import UserAdmin:
Certainly! The django.contrib.auth.admin module, specifically the UserAdmin class within it, provides default functionalities to manage user models within the Django admin interface.
6) Django-signals:
django signals is an event or action used to perform pre post actiions or event as soon as data is triggered into the database
7) form.forms hame tb use krna h jab model me fields na batai ho or shru se fields describe kr rhe ho form me hi...modelform tb use krte jab model tyaar ho bs form ki fields chahiye ho
8) request.POST['sth'] will raise a KeyError exception if 'sth' is not in request.POST.
request.POST.get('sth') will return None if 'sth' is not in request.POST
9) from django.contrib import messages , auth    # if we use this then views name can be login or logout and call it using auth.login() auth.logout auth.authenticate

from django.contrib.auth import authenticate , login , logout     #if we use this library then veiws name donot be login or logout and call it with auth.

10) 
The difference between password=request.POST.get('password') and password=form.cleaned_data['password'] lies in how they retrieve the password inputted by the user in the registration form.

a) password=request.POST.get('password'):
This line directly accesses the password field from the POST data submitted by the user.
It retrieves the password without performing any validation or cleaning. It simply gets the raw input as it was submitted.
This approach doesn't involve Django's form validation process, so the password may not be validated or cleaned according to any form field specifications you've defined.
b) password=form.cleaned_data['password']:
This line accesses the password field from the cleaned_data attribute of the form.
Before accessing the password, Django has already validated and cleaned the form data through its form validation process, ensuring that the password meets any validation rules you've defined in your form class.
Using cleaned_data ensures that you're working with sanitized and validated data, reducing the risk of errors or security vulnerabilities due to improperly formatted or invalid data.
In summary, request.POST.get('password') retrieves the raw, unvalidated input from the POST request, while form.cleaned_data['password'] retrieves the validated and cleaned password from the form's cleaned_data attribute. It's generally safer and more reliable to use form.cleaned_data['password'] because it ensures that you're working with validated data.

11) class Author(models.Model):
        name = models.CharField(max_length=100)

    class Book(models.Model):
        author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
        title = models.CharField(max_length=100)
    
    In this example, Book has a ForeignKey to Author, meaning each book is associated with one author. The related_name='books' attribute in the Book model specifies the name of the reverse relation from Author back to Book. So, if you have an Author object author, you can access all the books written by that author using author.books.

    If related_name is not specified, Django automatically creates a related name by appending _set to the lowercase name of the related model. In this example, if related_name wasn't specified, you would access the books through author.book_set instead of author.books.

    Using related_name allows you to provide a more descriptive name for the reverse relation, making your code more readable and understandable.

12) User.objects.get and User._default_manager.get are same
13) request.session['uid'] = uid  sessions are helpful to store user information to long term
14) Yes, you're correct. In the context of the save() method of a Django model, self.name or self.is_approved will give you the values of those fields after 
    the save    button is triggered and the changes are being saved to the database.
    self.. represents the current instance of the Vendor object.
    orig.. represents the instance of the Vendor object as it exists in the database before any changes were made to the current instance (self).
    'orig.is_approved' represents the value of is_approved in the database before any changes were made.
    'self.is_approved' represents the current value of is_approved in the instance being saved.
15) context processors... isme jo kxh bhi likhnge wo pore templates me hr html file k liye mojud hoka.nake srf ek view k liye
16) vendor_license = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info'})) add this in form class to load the css of image field
17) if you are making form with __all__ fields make sure dont forget to exclude the already forighn key field.otherwise it will give error while saving the form.
18) custom validators for image file extensions...

    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info'})) #if we dont use validators simply use imagefield
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator]) # if we use validators use filefield for image field otherwise it will give error on imagefield
19)     category = get_object_or_404(Category , pk=pk)  #getting category by pk
        fooditems = FoodItem.objects.filter(vendor=vendor , category=category) #searching by category and vendor from both
20)      vendor_name=v_form.cleaned_data['vendor_name']
        vendor.vendor_slug=slugify(vendor_name)+'-'+str(user.id)  # vendor name unique nai h to slug field unique kr rhe hn id k sth take same vendor name jab register ho to problem na aye

21) fooditems = category.fooditem_set.all() #gives all fooditems for one perticular category using model name
    # Get all food items for this category using the related_name 'food_items' in foreighn key
    food_items = category.food_items.all()
    # use prefetch method if you have any query for example i want all foods who is avilable this will give all category and as well ass all fooditems which are available
        categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset= FoodItem.objects.filter(is_available=True)
        )
    )
    # all categories and all food items
    categories = Category.objects.prefetch_related('food_items').all()  #food_items is the related_name of foreighn key in fooditems model it fetches all categories and their relted fooditems of each category
    # all categories and all fooditems in html template using for loop
    categories = Category.objects.filter(vendor=vendor) #in views
        {% for category in categories %}
            {{category}}
             {% for food in category.fooditems.all %} #relatedname is set to fooditems so we are using this if not (category.fooditem_set.all) now the fooditem is the model name and set is by default provide by django
                {{food}}
             {% endfor %}
        {% endfor %}   

22) #modify category to show only category own particular vendor in add food.html
    form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))  

23)  # this line below get all vendors which contains the fooditem....value_list('vendor',flat=true) flat gives pure simple list rather than list of tuples...if use only values('vendor') it give dict
fetch_all_vendor_ids_by_foodname = FoodItem.objects.filter(food_title__icontains = get_search ,            is_available = True).values_list('vendor' , flat=True)  



















<!--! steps) -->
install env , requirements, django or other stuff..and implement template then go to further steps
1) githubs setup and .gitignore file
2) postgress database integrations in settings install pyscobj2 and implement decouple to store sensitive information in settings
3) Custom usermodel & make password noneditable
4) profile model & django signals
5) customer registeration template inheritace and django forms & views, saving form & generating fields & non fields error of forms
6) django messages
7) Vendor registeration models,template, form, views , adminconfig (registering vendor with 2 forms in views)
8) login logout feature & detect user role to redirect thier specific dashboard customer or vendor using custom decorators (create function getrole in models)
9) ~Email configuration in settings then setup email verification function in views for registering and activating customer and 
    vendor. function defination in utils.py
    activate url with uidb64 and token and create view for activating the user
    password reseting...forgot password page and view checking if user exists with email if eit does send verificatio email
    after click link reset_password_validate func will check and store the id in session..finally reset password view will change the password..
10) approving vendor...creating save trigger function in vendors models when the is_approved is check or uncheck the         send_notfication_email function should trigger.
setup cust and vendor dashboard,setting vendor dashboard url setup.
context processors for cover and profile pic on every page..create context_processors file and write a function and dont forget to write in settings.py file in templates.always write code in try catch in context processor function
11) vendor profile setup..page and vendorprofileform setup and views ... showing form instance and loading image field css by putting one line code in form.py class ...making custom validators for images valid file extension...making latitude and longitude readonly field
12) google cloud billing section was skipped
13) setup new app menu create model class category and fooditem and setup adminpanel,,making form and adding category by form performing crud operations add update delete to category
14) error during adding same category from diff vendor..remove unique in models from category_name(personal prefference)
15) add food crud ,,showing category of loggedin user rather than showing all..fixing issue of profile pic and cover for new user like put in if condition so if there then it will show
16) create new app marketplace show vendor on home page ..add slug field on models and update the registerVendor form to auto create slug field..concotenate the id with slug field in registerVendor because vendor name is not unique and slug should be unique....
now implement slug into url of marketplace to go vendor details page and fetch vendor details
17) add to cart model , url ,views and write custom js on add to cart button,,add attribute data-url,data-id in ad to cart button...write ajax code in custom.js and check it is working in views..write code in try except block to increase the cart or create the cart
create context_processor for cart count and write code then fetch to navbar template...
place food quantity on each food access cart_items.quantity in vendor detail page and views and make for loop using empty span with the data-id and data-url...data-id should be same in both div which is in vendor detail looping food item..final wirte jquery to access span tag and push the quantity in fooditems loop...update the cart counter and quantity in real time pass jsonresponse...
decrease cart feature same as add to cart,create url view decrease ajax but only check if chkcart>1 then chkcart.quantity -= 1 in view....
implement sweetalert for json response
18) cart page url and template setup..showing cart items in cart page..delete cart item and removing item without reloading the page...decreasing cart after 0 remove with ajax also...context processor for subtotal tax and total...call getcartamount function in addtocart,decrease or delete ajax request
19) search url and view and search queries by restaurant name or fooditem both
20) opening hours urls views template sidebar,,,forms .. for adding without reloading the page set add hours url and views and then set ajax request...take all the values from html and also scrf token and send to ajax data..ajax will send data to view...ajax has data{} which send the data to view and get it from request.POST.get...create and save the data to database in view and send response to ajax..
removing ajax..
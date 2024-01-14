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









<!--! steps) -->
install env , requirements, django or other staff..and implement template then go to further steps
1) githubs setup and .gitignore file
2) postgress database integrations in settings and implement decouple to store sensitive information in settings
3) Custom usermodel $ make password noneditable
4) profile model & django signals
5) customer registeration template and django forms & views saving form & ,generating fields & non fields error of forms
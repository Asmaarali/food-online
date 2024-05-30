# from django.forms import ModelForm
from django import forms
# from django.forms import ModelForm 
from .models import User , UserProfile
from .validators import allow_only_images_validator


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "confirm_password",
        ]

    # generating non fields errors
    def clean(self):  # clean is a method builtin
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("password doesnot matched!")
        

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator]) # for adding css class directly for imagefield
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}),validators=[allow_only_images_validator]) 
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'start typing','required':'required'}))
    #making readonly input 1st method
    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'})) 
    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'})) 
    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ['user']
        
    
    # making readonly input 2nd method but usefull in complexx scenarios
    def __init__(self, *args, **kwargs):
        super(UserProfileForm,self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'
    
    
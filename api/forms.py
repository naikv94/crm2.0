from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Company, Contact, Profile

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']
        
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name','country','headquarters']
        exclude = ['user_id',]

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['contact_name','company','contact_number']
        exclude = ['user_id',]
    
    def clean_contact_number(self):
            contact_number = self.cleaned_data['contact_number']
            num = str(contact_number)
            if len(num) != 10 or len(num) < 10:
                raise forms.ValidationError("Check contact number.")
            return contact_number

        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'bio',
            'phone_number',
            'birth_date',
            'profile_image'
        ]

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
        ]


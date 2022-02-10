from django.contrib import admin
from .models import Company, Contact, Profile

# Register your models here.
@admin.register(Company)
class ComanyAdmin(admin.ModelAdmin):
    list_display = ['user_id','name','country','headquarters']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['user_id','contact_name','company','contact_number']
    search_fields = ['contact_name','company__name']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','bio','phone_number','birth_date','profile_image']
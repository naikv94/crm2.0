from django.shortcuts import render, redirect
from .forms import RegisterForm, CompanyForm, ContactForm, ProfileForm, UserForm
from django.contrib import messages
from .models import Contact, Company, Profile
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.models import User


def home(request):
    return render(request,'common/home.html')

@login_required(login_url='accounts/login/')
def dashboard(request):
    companies = Company.objects.filter(user_id = request.user.id).count()
    contacts = Contact.objects.filter(user_id = request.user.id).count()
    context = {
        'companies' : companies,
        'contacts' : contacts
    }
    return render(request,'common/dashboard.html', context)

##### Signup Views ######

def registerView(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request,'Register user Sucessfully')
            return render(request,'common/login.html')
        else:
            return render(request,'common/register.html',{'form':register_form})
    register_form = RegisterForm()
    return render(request,'common/register.html',{'form':register_form})


##### Dashboard Views #####
@login_required(login_url='accounts/login/')
def companyView(request):
    query = request.GET.get('q')
    user_id = request.user.id or None
    if user_id:
        company_data = Company.objects.filter(user_id = user_id)
        company_form = CompanyForm()
        if query:
            company_data = Company.objects.filter(user_id = user_id).filter(Q(name__icontains=query) | Q(headquarters__icontains=query)).order_by('id')
        else:
            company_data = Company.objects.all().order_by('id')
        context = {
            'data' : company_data,
            'form' : company_form,
        }
        context = paginationView(request, company_data, company_form)

        if request.method == 'POST':
            user = Company(user_id = user_id)
            company_form = CompanyForm(request.POST, instance=user)
            if company_form.is_valid():
                print('cleaned data',company_form.cleaned_data)
                company_form.save()
                messages.success(request, 'Company data added!!')
                return render(request,'common/companies.html', context)
            else:
                context['form'] = company_form
                return render(request,'common/companies.html', context)
        return render(request,'common/companies.html', context)
    return render(request,'common/companies.html', {})
    
@login_required(login_url='accounts/login/')
def contactView(request):
    user_id = request.user.id or None
    query = request.GET.get('q')
    if user_id:
        contact_data = Contact.objects.filter(user_id = user_id)
        contact_form = ContactForm()
        if query:
            contact_data = Contact.objects.filter(user_id = user_id).filter(Q(contact_name__icontains=query) | Q(company__name__icontains=query)).order_by('id')
        else:
            contact_data = Contact.objects.all().order_by('id')
        context = {
            'data' : contact_data,
            'form' : contact_form
        }
        context = paginationView(request, contact_data, contact_form)

        if request.method == 'POST':
            contact_form = ContactForm(request.POST)
            if contact_form.is_valid():
                contact_form.save()
                messages.success(request, 'Contact added!!')
                return render(request,'common/contacts.html', context)
            else :
                context['form'] = contact_form
                return render(request,'common/contacts.html', context)
        return render(request,'common/contacts.html', context)
    return render(request,'common/contacts.html', {})

@login_required(login_url='accounts/login/')
def companyDeleteView(request, id):
    id = id or None
    if id:
        data_to_delete = Company.objects.get(id = id)
        data_to_delete.delete()
        messages.success(request, 'Data deleted!!')
        return redirect('companies')
    messages.error(request, 'Invalid data!!')
    return redirect('companies')

@login_required(login_url='accounts/login/')
def companyUpdateView(request, id):
    id = id or None
    if request.method == 'POST':
        if id:
            data_to_update = Company.objects.get(id = id)
            company_form = CompanyForm(request.POST, instance=data_to_update)
            if company_form.is_valid():
                company_form.save()
                messages.success(request, 'Data updated!!')
                return redirect('companies')
            else:
                context = {
                    'form' : company_form
                }
                return render(request, 'common/companyUpdate.html', context)
    instance = Company.objects.get(id = id)
    company_form = CompanyForm(instance=instance)
    context = {
        'form' : company_form
    }
    return render(request, 'common/companyUpdate.html', context)

@login_required(login_url='accounts/login/')
def contactDeleteView(request, id):
    id = id or None
    if id:
        data_to_delete = Contact.objects.get(id = id)
        data_to_delete.delete()
        messages.success(request, 'Data deleted!!')
        return redirect('contacts')
    messages.error(request, 'Invalid data!!')
    return redirect('contacts')

@login_required(login_url='accounts/login/')
def contactUpdateView(request, id):
    id = id or None
    if request.method == 'POST':
        if id:
            data_to_update = Contact.objects.get(id = id)
            contact_form = ContactForm(request.POST, instance=data_to_update)
            if contact_form.is_valid():
                contact_form.save()
                messages.success(request, 'Data updated!!')
                return redirect('contacts')
            else:
                context = {
                    'form' : contact_form
                }
                return render(request, 'common/contactUpdate.html', context)
    instance = Contact.objects.get(id = id)
    contact_form = ContactForm(instance=instance)  #Prepopulating existing data
    context = {
        'form' : contact_form
    }
    return render(request, 'common/contactUpdate.html', context)

############################################################

def profile(request):
    context = {
        'user' : request.user,
    }
    return render(request, 'common/profile.html', context)

def profileUpdate(request):
    instance = User.objects.get(id = request.user.id)
    user_form = UserForm(instance=instance)
    instance = Profile.objects.get(user = request.user)
    profile_form = ProfileForm(instance=instance)
    context = {
        'user_form' : user_form,
        'profile_form' : profile_form
    }

    if request.method == 'POST':
        instance = User.objects.get(id = request.user.id)
        user_form = UserForm(request.POST, instance=instance)
        instance = Profile.objects.get(user = request.user)
        profile_form = ProfileForm(request.POST, instance=instance)
        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Profile updated')
            return redirect('profile')
        else:
            context['profile_form'] = profile_form
            context['user_form'] = user_form
            return render(request, 'common/profile-update.html', context)
            
    return render(request, 'common/profile-update.html', context)

###################### Pagination Function ###########################

def paginationView(request, data, form):
    page_number = request.GET.get('page')
    paginator = Paginator(data, 4)
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj' : page_obj,
        'paginator' : paginator,
        'form' : form
    }
    return context
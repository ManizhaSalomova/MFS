from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.shortcuts import render, get_object_or_404

from django.db.models import Sum
from _decimal import Decimal


from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect


now = timezone.now()
def home(request):
     return render(request, 'crm/home.html',
                 {'crm': home})


@login_required
def customer_list(request):
    customer = Customer.objects.filter(created_date__lte=timezone.now())
    return render(request, 'crm/customer_list.html',
                 {'customers': customer})


@login_required
def customer_edit(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   if request.method == "POST":
       # update
       form = CustomerForm(request.POST, instance=customer)
       if form.is_valid():
           customer = form.save(commit=False)
           customer.updated_date = timezone.now()
           customer.save()
           customer = Customer.objects.filter(created_date__lte=timezone.now())
           return render(request, 'crm/customer_list.html',
                         {'customers': customer})
   else:
        # edit
       form = CustomerForm(instance=customer)
   return render(request, 'crm/customer_edit.html', {'form': form})

@login_required
def customer_delete(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   customer.delete()
   return redirect('crm:customer_list')

@login_required
def service_list(request):
   services = Service.objects.filter(created_date__lte=timezone.now())
   return render(request, 'crm/service_list.html', {'services': services})

@login_required
def service_delete(request, pk):
   service = get_object_or_404(Service, pk=pk)
   service.delete()
   return redirect('crm:service_list')

@login_required
def service_new(request):
   if request.method == "POST":
       form = ServiceForm(request.POST)
       if form.is_valid():
           service = form.save(commit=False)
           service.created_date = timezone.now()
           service.save()
           services = Service.objects.filter(created_date__lte=timezone.now())
           return render(request, 'crm/service_list.html',
                         {'services': services})
   else:
       form = ServiceForm()
       # print("Else")
   return render(request, 'crm/service_new.html', {'form': form})

@login_required
def service_edit(request, pk):
   service = get_object_or_404(Service, pk=pk)
   if request.method == "POST":
       form = ServiceForm(request.POST, instance=service)
       if form.is_valid():
           service = form.save()
           # service.customer = service.id
           service.updated_date = timezone.now()
           service.save()
           services = Service.objects.filter(created_date__lte=timezone.now())
           return render(request, 'crm/service_list.html', {'services': services})
   else:
       # print("else")
       form = ServiceForm(instance=service)
   return render(request, 'crm/service_edit.html', {'form': form})



@login_required
def product_list(request):
   products = Product.objects.filter(created_date__lte=timezone.now())
   return render(request, 'crm/product_list.html', {'products': products})

@login_required
def product_delete(request, pk):
   product = get_object_or_404(Product, pk=pk)
   product.delete()
   return redirect('crm:product_list')

@login_required
def product_new(request):
   if request.method == "POST":
       form = ProductForm(request.POST)
       if form.is_valid():
           product = form.save(commit=False)
           product.created_date = timezone.now()
           product.save()
           products = Product.objects.filter(created_date__lte=timezone.now())
           return render(request, 'crm/product_list.html',
                         {'products': products})
   else:
       form = ProductForm()
       # print("Else")
   return render(request, 'crm/product_new.html', {'form': form})

@login_required
def product_edit(request, pk):
   product = get_object_or_404(Product, pk=pk)
   if request.method == "POST":
       form = ProductForm(request.POST, instance=product)
       if form.is_valid():
           product = form.save()
           # service.customer = service.id
           product.updated_date = timezone.now()
           product.save()
           products = Product.objects.filter(created_date__lte=timezone.now())
           return render(request, 'crm/product_list.html', {'products': products})
   else:
       # print("else")
       form = ProductForm(instance=product)
   return render(request, 'crm/product_edit.html', {'form': form})

@login_required
def summary(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customers = Customer.objects.filter(created_date__lte=timezone.now())
    services = Service.objects.filter(cust_name=pk)
    products = Product.objects.filter(cust_name=pk)
    sum_service_charge = Service.objects.filter(cust_name=pk).aggregate(Sum('service_charge'))
    if(sum_service_charge['service_charge__sum'] == None):
        sum_service_charge['service_charge__sum'] =0
    print(sum_service_charge)
    sum_product_charge = Product.objects.filter(cust_name=pk).aggregate(Sum('charge'))
    if (sum_product_charge['charge__sum'] == None):
        sum_product_charge['charge__sum'] = 0
    print(sum_product_charge)
    return render(request, 'crm/summary.html', {'products': products,
                                                'services': services,
                                                'sum_service_charge': sum_service_charge,
                                                'sum_product_charge': sum_product_charge,
                                                'thecustomer':customer,
                                                })

#def change_password(request):
 #   if request.method == 'POST':
  #      form = PasswordChangeForm(request.user, request.POST)
   #     if form.is_valid():
    #        user = form.save()
     #       update_session_auth_hash(request, user)  # Important!
      #      messages.success(request, 'Your password was successfully updated!')
       #     return redirect('change_password')
        #else:
         #   messages.error(request, 'Please correct the error below.')
    #else:
     #   form = PasswordChangeForm(request.user)
    #return render(request, 'registration/change_password.html', {
     #   'form': form
    #})
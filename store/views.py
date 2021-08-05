from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .forms import *
from .models import *
from .decorators import *
from django.template import loader
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
import json
@allowed_user(allow_roles=['admins'])
def index(request):
    return HttpResponse('<h1>Bu muhim sahifa</h1>')

def categories(request):
    cat_list = Categories.objects.all()
    context = {
        'cat_list':cat_list,
        'tot_ord': get_total_order(request)
    }
    template  = loader.get_template('store/categories.html')
    return HttpResponse(template.render(context,request))
@login_required(login_url = 'login')
def products(request,cat_id):
    pds = Products.objects.filter(category=cat_id)
    context = {
        'pd_list': pds,
        'tot_ord': get_total_order(request)
    }
    template = loader.get_template('store/products.html')
    return HttpResponse(template.render(context, request))

def cart(request):
    customer, created = Customer.objects.get_or_create(user=request.user)
    orders = Orders.objects.filter(customer=customer)
    order_dets = []
    for order in orders:
        for od in Order_details.objects.filter(order = order):
            order_dets.append(od)
    s,q = 0,0
    for i in order_dets:
        s += i.total
        q += i.quantity
    context = {
        'ords':order_dets,
        'summ':s,
        'quantity':q,
        'tot_ord': get_total_order(request)
    }
    template = loader.get_template('store/cart.html')
    return HttpResponse(template.render(context, request))
def user_cart(request,id):
    customer = Customer.objects.get(pk=id)
    orders = Orders.objects.filter(customer=customer)
    order_dets = []
    for order in orders:
        for od in Order_details.objects.filter(order = order):
            order_dets.append(od)
    s,q = 0,0
    for i in order_dets:
        s += i.total
        q += i.quantity
    context = {
        'ords':order_dets,
        'summ':s,
        'quantity':q,
        'tot_ord': get_total_order(request),
        'current_user':customer.user.username
    }
    template = loader.get_template('store/user_cart.html')
    return HttpResponse(template.render(context, request))
def update_details(request):
    customer,created = Customer.objects.get_or_create(user=request.user)
    customer.save()
    data = json.loads(request.body)
    order,created = Orders.objects.get_or_create(customer=customer)
    order.save()
    pd = Products.objects.get(id = data['product_id'])
    order_detail,created = Order_details.objects.get_or_create(product = pd,order = order)
    order_detail.save()
    if data['action']=='add':
            order_detail.quantity += 1
    elif data['action']=='remove':
        if order_detail.quantity == 0:
            order_detail.delete()
        else:
            order_detail.quantity -= 1
    order_detail.save()
    if order_detail.quantity<=0:
        order_detail.delete()
    return JsonResponse('order_detail yangilandi',safe=False)

def get_total_order(request):
    customer,created = Customer.objects.get_or_create(user = request.user)
    orders = Orders.objects.filter(customer = customer)
    s = 0
    for order in orders:
        order_details = Order_details.objects.filter(order = order)
        s += sum([o.quantity for o in order_details])
    return s

def user_form(request):
    print(request.POST)
    form = createUserForm()
    if request.method == 'POST':
        form = createUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {
        'form':form
    }
    return render(request,'store/user_form.html',context)
def product_form(request):
    print(request.POST)
    form = ProductForm(request.POST,request.FILES)
    print(form.is_valid())
    if form.is_valid():
        form.save()
    context = {
        'form':form
    }
    return render(request,'store/product_form.html',context)
@unauthenticated
def log_in(request):
    print(request.POST)
    form = Login()
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request,username = username, password = password)
    if user:
        login(request,user)
        return redirect('cart')
    context = {
        'form': form
    }
    return render(request, 'store/user_form.html', context)
def log_out(request):
    logout(request)
    return redirect('login')
def client_orders(request):
    customers = Customer.objects.all()
    datas = dict()
    for customer in customers:
        orders = Orders.objects.filter(customer=customer)
        s = 0
        for order in orders:
            order_details = Order_details.objects.filter(order=order)
            s += sum([o.quantity for o in order_details])
        datas[customer.id] = s
    context = {
        'customers': customers,
        'datas': get_total_order(request)
    }
    print(datas)
    return render(request,'store/client_orders.html',context)
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import QuerySet
from django.urls import reverse
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import OrderForm, InterestForm, SignUpForm
from .models import Client, Category, Product, Order


# Create your views here.
def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    product_list = Product.objects.all().order_by('-price')[:5]
    response = HttpResponse()
    heading1 = '<p>' + 'List of categories: ' + '</p>'
    response.write(heading1)
    for category in cat_list:
        para = '<p>' + str(category.id) + ': ' + str(category) + '</p>'
        response.write(para)

    # products upto 5, sorted in descending order of price
    heading2 = '<p>' + 'List of products: ' + '</p>'
    response.write(heading2)
    for product in product_list:
        para1 = '<p>' + str(product.id) + ': ' + str(product) + '</p>'
        response.write(para1)

    return render(request, 'webocr/index.html', {'cat_list': cat_list})


def about(request):
    max_age = 60 * 5
    response = render(request, "webocr/about.html", {'about_visits': request.COOKIES.get('about_visits')})
    print(request.COOKIES.get('about_visits'))
    if request.COOKIES.get('about_visits'):
        increment = int(request.COOKIES['about_visits']) + 1
        response.set_cookie('about_visits', increment, max_age)
    else:
        response.set_cookie('about_visits', 1, max_age)
    return response


def detail(request, cat_no):
    response = HttpResponse()
    category = get_object_or_404(Category, pk=cat_no)
    prod_list = Product.objects.filter(category_id=cat_no)

    heading1 = '<p>' + 'Warehouse: ' + str(category.warehouse) + '</p>'
    response.write(heading1)
    heading2 = '<p>' + 'Products for ' + category.name + ' with cat_no= ' + str(cat_no) + 'are: </p>'
    response.write(heading2)
    i = 1
    for product in prod_list:
        para = '<p>' + str(i) + '=' + str(product.name) + '</p>'
        response.write(para)
        i = i + 1
    return render(request, 'webocr/detail.html', {'cat_no': cat_no, 'category': category, 'prod_list': prod_list})


def products(request):
    prodlist = Product.objects.all().order_by('id')
    return render(request, 'webocr/products.html', {'prodlist': prodlist})


def placeorder(request):
    msg = ""
    prodlist = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.num_units <= order.product.stock:
                product = Product.objects.get(pk=order.product.id)
                product.stock -= order.num_units
                product.save()
                order.save()
                msg = 'Your order has been placed successfully.'
                print("true")
                order.product.stock -= order.num_units
            else:
                msg = 'We do not have sufficient stock to fill your order.'
                print("False")
            return render(request, 'webocr/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'webocr/placeorder.html', {'form': form, 'msg': msg, 'prodlist': prodlist})


def productdetail(request, prod_id):
    cat_list = Category.objects.all().order_by('id')[:10]
    form = InterestForm()
    product_info = get_object_or_404(Product, pk=prod_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            print(">>>>>>>>>>>." + request.POST["interested"])
            if request.POST["interested"]:
                product = Product.objects.get(pk=prod_id)
                product.interested += 1
                product.save()
            return HttpResponseRedirect("/webocr/")

    return render(request, 'webocr/productdetail.html', {'prod_info': product_info, 'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                last_login = str(datetime.now())
                request.session.set_expiry(3600)
                request.session['last_login'] = last_login
                login(request, user)
                return HttpResponseRedirect(reverse('webocr:index'))
            # When I am logged in as auth user, I'll get the last_login info in index page.
            # When I am not logged in as auth user, I'll not get last_login info, as I have set the condition
            # accordingly in index.html.
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'webocr/login.html')


def user_register(request):
    a = Client()
    form = SignUpForm(request.POST, instance=a)
    if form.is_valid():
        form.save(commit=True)
        form.save_m2m()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('webocr:index')
    else:
        form = SignUpForm()
    return render(request, 'webocr/register.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('webocr:index'))


@login_required(redirect_field_name='next', login_url='/webocr/login/')
def my_orders(request):
    message = ''
    global ord
    if request.user:
        if request.user.is_authenticated:
            client_id = Client.objects.filter(first_name=request.user.first_name)
            if client_id:
                ord = Order.objects.filter(client_id=request.user.id)
                print(ord)
                if not ord:
                    message = 'You have not made any orders.'
            else:
                message = 'User is not registered as a client'
            print(client_id)
        return render(request, 'webocr/myorders.html', {'orders': ord})
    else:
        redirect('webocr:login')


def reset_password(request):
    if request.method == "POST":
        email = request.POST['email']
        user = User.objects.filter(email=email).first()
        if user:
            password = User.objects.make_random_password(length=14,
                                                         allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")  # zvk0hawf8m6394
            user.set_password(password)
            user.save()
            send_mail('Hello from Rahul', 'hello' + password, 'test.email2498@gmail.com', [email],
                      fail_silently=False)
            return render(request, 'webocr/password_email_successful.html')
        else:
            messages.error(request, 'User with this email not found.')

    return render(request, 'webocr/password_reset_form.html')


def password_changed(request):
    return render(request, 'webocr/password_email_successful.html')

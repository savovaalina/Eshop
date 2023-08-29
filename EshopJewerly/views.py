import json

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm, UserProfileForm, CategoryForm, ManufacturerForm, ProductForm, \
    UpdateQuantityForm
from .models import UserProfile, Product, Order, ShoppingCart, Category, Manufacturer
from django.db.models import Q
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from functools import wraps
from django.core.paginator import Paginator
from django.utils import timezone
from rest_framework.decorators import api_view
from django.core import serializers


# Create your views here.
def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.username == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/products')

    return _wrapped_view


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = UserProfile.objects.create(user=user)
            profile.save()
            cart = ShoppingCart.objects.create(user=user, dateCreated=timezone.now(), status="Active")
            cart.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def user_profiles(request):
    user = request.user
    profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        print("POST METHOD")
        if form.is_valid():
            form.save()
    else:
        form = UserProfileForm(instance=profile)

    context = {
        'user': user,
        'profile': profile,
        'form': form
    }

    return render(request, 'view_user_profile.html', context)


@login_required
def edit_profile(request):
    profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'profile_form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user2 = User.objects.get(username=username)

        if user2 is not None:
            login(request, user2)
            return redirect('home')  # Redirect to the home page
        else:
            return render(request, 'login.html',
                          {'username': username, 'error_message': 'Invalid username or password'})
    else:
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
@admin_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()

    context = {'form': form}
    return render(request, 'add_category.html', context)


@login_required
@admin_required
def category_list(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'category_list.html', context)


@login_required
@admin_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    # Handle editing category logic here
    return render(request, 'edit_category.html', {'category': category})


@login_required
@admin_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'delete_category.html', {'category': category})


@login_required
@admin_required
def add_manufacturer(request):
    if request.method == 'POST':
        form = ManufacturerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manufacturer_list')
    else:
        form = ManufacturerForm()

    context = {'form': form}
    return render(request, 'add_manufacturer.html', context)


@login_required
@admin_required
def manufacturer_list(request):
    manufacturers = Manufacturer.objects.all()
    return render(request, 'manufacturer_list.html', {'manufacturers': manufacturers})


@login_required
@admin_required
def edit_manufacturer(request, manufacturer_id):
    manufacturer = get_object_or_404(Manufacturer, pk=manufacturer_id)

    if request.method == 'POST':
        form = ManufacturerForm(request.POST, instance=manufacturer)
        if form.is_valid():
            form.save()
            return redirect('manufacturer_list')
    else:
        form = ManufacturerForm(instance=manufacturer)

    return render(request, 'edit_manufacturer.html', {'form': form, 'manufacturer': manufacturer})


@login_required
@admin_required
def delete_manufacturer(request, manufacturer_id):
    manufacturer = get_object_or_404(Manufacturer, pk=manufacturer_id)

    if request.method == 'POST':
        manufacturer.delete()
        return redirect('manufacturer_list')

    return render(request, 'delete_manufacturer.html', {'manufacturer': manufacturer})


@login_required
@admin_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Handle successful form submission
            return redirect('product_list')
    else:
        form = ProductForm()

    context = {'form': form, 'edit_mode': False}  # Pass edit_mode=False for adding
    return render(request, 'add_product.html', context)


@login_required
@admin_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            # Handle successful form submission
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    context = {'form': form, 'edit_mode': True}  # Pass edit_mode=True for editing
    return render(request, 'add_product.html', context)


@login_required
@admin_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        product.delete()
        return redirect('product_list')

    return render(request, 'delete_product.html', {'product': product})


@login_required
def place_order(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        address = request.POST.get('address', None)
        name = request.POST.get('name', None)
        surname = request.POST.get('surname', None)

        # Check if the address is not empty and not 'None'
        if address and address != 'None':
            quantity = int(request.POST.get('quantity', 1))
            print("POST ORDER");
            # Create the order
            order = Order.objects.create(
                user=request.user,
                name=name,
                surname=surname,
                total_price=product.price * quantity,
                quantity=quantity
            )
            print("ORDER CREATED", order.id)
            order.products.add(product)  # Add the product to the order's products

            # Perform any other necessary actions, like calculating total price, etc.
            return redirect('bought_products')

    context = {'product': product, 'user_profile': user_profile}
    return render(request, 'place_order.html', context)


@login_required
def place_order_multiple(request):
    ordered_products = []
    ordered_products_serialized = []

    if request.method == 'POST':
        print("POST PLACE ORDER MULTIPLE")
        address = request.POST.get('address', None)
        name = request.POST.get('name', None)
        surname = request.POST.get('surname', None)
        if address and address != 'None':
            ordered_products = [key.split('_')[1] for key in request.POST if key.startswith('product_')]
            user_profile = UserProfile.objects.get(user=request.user)
            print("ordreed products:", ordered_products)
            orders_created = []
            print("POST PLACE ORDER MULTIPLE with address pass")
            with transaction.atomic():
                print("at transcation")
                for product_id in ordered_products:
                    print("at for")
                    shopping_cart = ShoppingCart.objects.get(user=request.user)

                    quantity = int(request.POST.get('product_' + product_id + "_quantity"))
                    product = Product.objects.get(id=product_id)
                    shopping_cart.products.remove(product)
                    shopping_cart.save()
                    print("POST ORDER");
                    # Create the order
                    order = Order.objects.create(
                        user=request.user,
                        name=name,
                        surname=surname,
                        total_price=product.price * quantity,
                        quantity=quantity
                    )
                    print("ORDER CREATED", order.id)
                    order.products.add(product)
                    orders_created.append(order)

            return redirect('bought_products')

    else:
        orders_json = request.GET.get('orders')
        if orders_json:
            orders = json.loads(orders_json)
            # Process the orders as needed
            print("GET", orders)
            for ordered_product in orders:
                productId = ordered_product['productId']
                product = Product.objects.get(id=productId)
                ordered_product_serialized = {
                    'product_id': product.id,
                    'product_name': product.name,
                    'product_price': product.price,
                    'quantity': ordered_product['quantity'],
                    'total_price': product.price * int(ordered_product['quantity'])
                }
                ordered_products_serialized.append(ordered_product_serialized)
                user_profile = UserProfile.objects.get(user=request.user)
            context = {
                'ordered_products': ordered_products_serialized,
                'user_profile': user_profile
            }
            return render(request, 'place_order_multiple.html', context)
        else:
            # Handle the case when there are no orders in the query parameters
            context = {
                'message': 'This is the place order page for multiple products'
            }
            return render(request, 'place_order_multiple.html', context)


@login_required
def order_confirmation_modal(request, order_id):
    order = Order.objects.get(pk=order_id)
    return render(request, 'order_confirmation_modal.html', {'order': order})


@login_required
def shopping_cart(request):
    user = request.user
    try:
        shopping_cart = ShoppingCart.objects.get(user=user)
    except ShoppingCart.DoesNotExist:
        shopping_cart = ShoppingCart.objects.create(user=user, dateCreated=timezone.now(), status="Active")
    products = shopping_cart.products.all()
    return render(request, 'shopping_cart.html', {'products': products})


@login_required
def remove_from_cart(request, product_id):
    # Assuming you have a Cart model that contains products
    cart = ShoppingCart.objects.get(user=request.user)  # Adjust the retrieval of the cart based on your model structure
    product = get_object_or_404(Product, pk=product_id)

    # Remove the product from the cart
    cart.products.remove(product)
    cart.save()
    return redirect('shopping_cart')  #


@login_required
def bought_products(request):
    user = request.user
    bought_orders = Order.objects.filter(user=user)
    context = {
        'bought_orders': bought_orders,
    }

    return render(request, 'bought_products.html', context)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user_cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    user_cart.products.add(product)
    return redirect('shopping_cart')


@login_required
def update_quantity(request, product_id):
    shopping_cart = ShoppingCart.objects.get(user=request.user)
    product = Product.objects.get(pk=product_id)

    if request.method == 'POST':
        form = UpdateQuantityForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            shopping_cart.products.update_or_create(product=product, defaults={'quantity': quantity})
            return redirect('shopping_cart')
    else:
        initial_quantity = shopping_cart.products.through.objects.get(product=product).quantity
        form = UpdateQuantityForm(initial={'quantity': initial_quantity})

    return render(request, 'update_quantity.html', {'form': form, 'product': product})


def product_list(request):
    products = Product.objects.all()  # Get all products
    genders = Product.GENDER_CHOICES

    # Apply filters based on user selections
    search_query = request.GET.get('search')
    category_ids = request.GET.getlist('categories')
    gender_choices = request.GET.getlist('genders')
    manufacturer_ids = request.GET.getlist('manufacturers')

    if search_query:
        products = products.filter(name__icontains=search_query)

    if category_ids:
        products = products.filter(category_id__in=category_ids)

    if gender_choices:
        products = products.filter(gender__in=gender_choices)

    if manufacturer_ids:
        products = products.filter(manufacturer_id__in=manufacturer_ids)

    # Retrieve categories, genders, and manufacturers for filters
    categories = Category.objects.all()
    manufacturers = Manufacturer.objects.all()

    paginator = Paginator(products, per_page=20)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        'products': products,
        'categories': categories,
        'manufacturers': manufacturers,
        'genders': genders
    }

    return render(request, 'product_list.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}
    return render(request, 'product_detail.html', context)


@login_required
@admin_required
def orders_list(request):
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'orders.html', context)
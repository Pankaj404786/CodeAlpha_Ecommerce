from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import Product, Order, OrderItem

def _cart_products(request):
    cart = request.session.get("cart", {})
    products, total = [], Decimal("0.00")
    for product_id, quantity in cart.items():
        product = Product.objects.filter(pk=product_id).first()
        if not product:
            continue
        quantity = max(1, int(quantity))
        line_total = product.price * quantity
        products.append({"product": product, "quantity": quantity, "line_total": line_total})
        total += line_total
    return products, total

def home(request):
    products = Product.objects.all()
    return render(request, "shop/home.html", {"products": products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "shop/product_detail.html", {"product": product})

@require_POST
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.stock < 1:
        messages.error(request, "This product is currently out of stock.")
        return redirect("product_detail", pk=pk)
    cart = request.session.get("cart", {})
    key = str(product.pk)
    cart[key] = min(int(cart.get(key, 0)) + 1, product.stock)
    request.session["cart"] = cart
    messages.success(request, f"{product.name} added to your cart.")
    return redirect(request.POST.get("next") or "cart")

def cart_view(request):
    items, total = _cart_products(request)
    return render(request, "shop/cart.html", {"items": items, "total": total})

@require_POST
def update_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    try:
        quantity = int(request.POST.get("quantity", "1"))
    except ValueError:
        quantity = 1
    cart = request.session.get("cart", {})
    if quantity <= 0:
        cart.pop(str(pk), None)
    else:
        cart[str(pk)] = min(quantity, product.stock)
    request.session["cart"] = cart
    return redirect("cart")

@require_POST
def remove_from_cart(request, pk):
    cart = request.session.get("cart", {})
    cart.pop(str(pk), None)
    request.session["cart"] = cart
    return redirect("cart")

@login_required
def checkout(request):
    items, total = _cart_products(request)
    if not items:
        messages.info(request, "Your cart is empty.")
        return redirect("home")
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        address = request.POST.get("address", "").strip()
        if not all([full_name, email, address]):
            messages.error(request, "Please complete all delivery fields.")
            return render(request, "shop/checkout.html", {"items": items, "total": total})
        with transaction.atomic():
            # Re-check stock before accepting the order.
            for item in items:
                product = Product.objects.select_for_update().get(pk=item["product"].pk)
                if product.stock < item["quantity"]:
                    messages.error(request, f"Not enough stock for {product.name}. Please update your cart.")
                    return redirect("cart")
            order = Order.objects.create(
                user=request.user, full_name=full_name, email=email,
                address=address, total=total
            )
            for item in items:
                product = Product.objects.select_for_update().get(pk=item["product"].pk)
                OrderItem.objects.create(
                    order=order, product=product, product_name=product.name,
                    price=product.price, quantity=item["quantity"]
                )
                product.stock -= item["quantity"]
                product.save(update_fields=["stock"])
        request.session["cart"] = {}
        messages.success(request, f"Order #{order.pk} placed successfully.")
        return redirect("my_orders")
    return render(request, "shop/checkout.html", {"items": items, "total": total})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items")
    return render(request, "shop/my_orders.html", {"orders": orders})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "shop/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(request.GET.get("next") or "home")
    else:
        form = AuthenticationForm(request)
    return render(request, "shop/login.html", {"form": form})

@require_POST
def logout_view(request):
    logout(request)
    return redirect("home")

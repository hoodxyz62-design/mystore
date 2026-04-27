from django.shortcuts import render, redirect
from .models import Product, Cart, Order


# Home page
def home(request):
    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    return render(request, 'home.html', {'products': products})


# Product detail
def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'product_detail.html', {'product': product})


# Add to cart
def add_to_cart(request, id):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    product = Product.objects.get(id=id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('/cart/')


# Cart page
def cart(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    items = Cart.objects.filter(user=request.user)

    total = 0
    for item in items:
        total += item.product.price * item.quantity

    return render(request, 'cart.html', {'items': items, 'total': total})


# Increase quantity
def increase_quantity(request, id):
    item = Cart.objects.get(id=id, user=request.user)
    item.quantity += 1
    item.save()
    return redirect('/cart/')


# Decrease quantity
def decrease_quantity(request, id):
    item = Cart.objects.get(id=id, user=request.user)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('/cart/')


# Remove item
def remove_from_cart(request, id):
    item = Cart.objects.get(id=id, user=request.user)
    item.delete()
    return redirect('/cart/')


# Checkout
def checkout(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    items = Cart.objects.filter(user=request.user)

    total = 0
    for item in items:
        total += item.product.price * item.quantity

    if request.method == 'POST':
        address = request.POST.get('address')

        for item in items:
            Order.objects.create(
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                address=address
            )

        items.delete()

        return render(request, 'success.html')

    return render(request, 'checkout.html', {
        'items': items,
        'total': total
    })


# Orders page
def orders(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders.html', {'orders': orders})


# Cancel order
def cancel_order(request, id):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    order = Order.objects.get(id=id, user=request.user)
    order.status = "Cancelled"
    order.save()

    return redirect('/orders/')

def buy_now(request, id):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    product = Product.objects.get(id=id)

    if request.method == 'POST':
        address = request.POST.get('address')

        Order.objects.create(
            user=request.user,
            product=product,
            quantity=1,
            address=address
        )

        return render(request, 'success.html')

    return render(request, 'checkout.html', {
        'items': None,
        'single_product': product,
        'total': product.price
    })
    
    
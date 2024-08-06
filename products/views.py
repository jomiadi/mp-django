from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order
from django.http import JsonResponse

def filter_products(request):
    filter_type = request.GET.get('filter_type')
    filter_value = request.GET.get('filter_value')

    if filter_type == 'bank':
        products = Product.objects.filter(bank=filter_value)
        liquid_products = Product.objects.filter(bank=filter_value).order_by('-liquidity')[:10]
    elif filter_type == 'geo':
        products = Product.objects.filter(geo=filter_value)
        liquid_products = Product.objects.filter(geo=filter_value).order_by('-liquidity')[:10]
    elif filter_type == 'goal':
        products = Product.objects.filter(goal=filter_value)
        liquid_products = Product.objects.filter(goal=filter_value).order_by('-liquidity')[:10]
    else:
        products = Product.objects.all()
        liquid_products = Product.objects.order_by('-liquidity')[:10]

    product_data = list(products.values('id', 'name', 'description', 'price', 'owner__username'))
    liquid_product_data = list(liquid_products.values('id', 'name', 'description', 'liquidity'))

    return JsonResponse({'products': product_data, 'liquid_products': liquid_product_data})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    buy_orders = Order.objects.filter(product=product, order_type='buy')
    sell_orders = Order.objects.filter(product=product, order_type='sell')

    bank_filter = request.GET.get('bank')
    geo_filter = request.GET.get('geo')
    goal_filter = request.GET.get('goal')

    if bank_filter:
        buy_orders = buy_orders.filter(bank=bank_filter)
        sell_orders = sell_orders.filter(bank=bank_filter)
    if geo_filter:
        buy_orders = buy_orders.filter(geo=geo_filter)
        sell_orders = sell_orders.filter(geo=geo_filter)
    if goal_filter:
        buy_orders = buy_orders.filter(goal=goal_filter)
        sell_orders = sell_orders.filter(goal=goal_filter)

    context = {
        'product': product,
        'buy_orders': buy_orders,
        'sell_orders': sell_orders,
        'banks': Product.objects.values_list('bank', flat=True).distinct(),
        'geos': Product.objects.values_list('geo', flat=True).distinct(),
        'goals': Product.objects.values_list('goal', flat=True).distinct(),
    }
    return render(request, 'products/product_detail.html', context)

def home(request):
    bank_filter = request.GET.get('bank')
    geo_filter = request.GET.get('geo')
    goal_filter = request.GET.get('goal')

    products = Product.objects.all()
    if bank_filter:
        products = products.filter(bank=bank_filter)
    if geo_filter:
        products = products.filter(geo=geo_filter)
    if goal_filter:
        products = products.filter(goal=goal_filter)

    banks = Product.objects.values_list('bank', flat=True).distinct()
    geos = Product.objects.values_list('geo', flat=True).distinct()
    goals = Product.objects.values_list('goal', flat=True).distinct()

    liquid_products = products.order_by('-liquidity')[:5]

    context = {
        'products': products,
        'banks': banks,
        'geos': geos,
        'goals': goals,
        'liquid_products': liquid_products
    }
    return render(request, 'home.html', context)

@login_required(login_url='/users/login/')
def create_order(request, product_id, order_type):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        price = request.POST['price']
        quantity = request.POST['quantity']
        currency = request.POST['currency']
        Order.objects.create(product=product, user=request.user, order_type=order_type, price=price, quantity=quantity, currency=currency)
        return redirect('product_detail', pk=product_id)
    return render(request, 'products/create_order.html', {'product': product, 'order_type': order_type})

@login_required(login_url='/users/login/')
def active_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'products/active_orders.html', {'orders': orders})

def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'products/order_detail.html', {'order': order})

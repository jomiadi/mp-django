from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Product, Order

def filter_products(request):
    filter_type = request.GET.get('filter_type')
    filter_value = request.GET.get('filter_value')

    filters = {
        'geo': 'geo',
        'goal': 'goal'
    }

    if filter_type in filters:
        products = Product.objects.filter(**{filters[filter_type]: filter_value})
        liquid_products = products.order_by('-liquidity')[:10]
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
    buy_orders, sell_orders = filter_orders(request, product)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'buy_orders': list(buy_orders.values('user__username', 'quantity', 'price', 'currency')),
            'sell_orders': list(sell_orders.values('user__username', 'quantity', 'price', 'currency'))
        })

    context = {
        'product': product,
        'buy_orders': buy_orders,
        'sell_orders': sell_orders,
        'geos': Product.objects.values_list('geo', flat=True).distinct(),
        'goals': Product.objects.values_list('goal', flat=True).distinct(),
    }
    return render(request, 'products/product_detail.html', context)

def filter_orders(request, product):
    buy_orders = Order.objects.filter(product=product, order_type='buy')
    sell_orders = Order.objects.filter(product=product, order_type='sell')

    filters = {
        'geo': request.GET.get('geo'),
        'goal': request.GET.get('goal')
    }

    for filter_type, filter_value in filters.items():
        if filter_value:
            buy_orders = buy_orders.filter(**{f'product__{filter_type}': filter_value})
            sell_orders = sell_orders.filter(**{f'product__{filter_type}': filter_value})

    return buy_orders, sell_orders

def home(request):
    filters = {
        'geo': request.GET.get('geo'),
        'goal': request.GET.get('goal')
    }

    products = Product.objects.all()
    for filter_type, filter_value in filters.items():
        if filter_value:
            products = products.filter(**{filter_type: filter_value})

    liquid_products = products.order_by('-liquidity')[:5]

    context = {
        'products': products,
        'geos': Product.objects.values_list('geo', flat=True).distinct(),
        'goals': Product.objects.values_list('goal', flat=True).distinct(),
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

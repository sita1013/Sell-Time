from django.shortcuts import render, redirect
from .models import TimePackage
from django.db.models import Min 

def homepage(request):
    return render(request, 'sell_time/homepage.html')

def product_list(request):
    future_packages = TimePackage.objects.filter(use_type='future').order_by('duration_minutes')
    past_packages = TimePackage.objects.filter(use_type='past').order_by('duration_minutes')
    if request.method == 'POST':
        package_id = request.POST.get('selected_package')
        if package_id:
            package = TimePackage.objects.get(id=package_id)
            cart = request.session.get('cart', [])
            cart.append({
                'name': package.name,
                'duration': package.duration_minutes,
                'price': float(package.price)
            })
            request.session['cart'] = cart
    return render(request, 'sell_time/product_list.html', {
        'future_packages': future_packages,
        'past_packages': past_packages,
    })

def cart(request):
    cart = request.session.get('cart', [])
    return render(request, 'sell_time/cart.html', {'cart': cart})

def clear_cart(request):
    request.session['cart'] = []
    return redirect('cart')

def graphs(request):
    return render(request, 'sell_time/graphs.html')
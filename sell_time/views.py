from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import TimePackage
from django.db.models import Min 

def homepage(request):
    return render(request, 'sell_time/homepage.html')

def product_list(request):
    if request.method == 'POST':
        package_id = request.POST.get('selected_package')
        if package_id:
            package = get_object_or_404(TimePackage, id=package_id)
            cart = request.session.get('cart', [])
            cart.append({
                'name': package.name,
                'duration': package.duration_minutes,
                'price': float(package.price)
            })
            request.session['cart'] = cart
    return render(request, 'sell_time/product_list.html')

def timepackage_search(request):
    q = request.GET.get('q', '')
    use_type = request.GET.get('type', 'future')
    packages = TimePackage.objects.filter(use_type=use_type, name__icontains=q).order_by('duration_minutes')[:20]
    data = [
        {
            'id': p.id,
            'text': f"{p.duration_minutes} min - £{p.price:.2f}"
        }
        for p in packages
    ]
    return JsonResponse({'results': data})
    if not data:
        return JsonResponse({'results': [], 'message': 'No matching packages found.'})


def cart(request):
    cart = request.session.get('cart', [])
    return render(request, 'sell_time/cart.html', {'cart': cart})

def clear_cart(request):
    request.session['cart'] = []
    return redirect('cart')

def graphs(request):
    return render(request, 'sell_time/graphs.html')
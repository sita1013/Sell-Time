from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import TimePackage
from django.db.models import Min 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView
from .forms import TimePackageForm
from django.urls import reverse_lazy

from faker import Faker

def homepage(request):
    return render(request, 'sell_time/homepage.html')

class SignUpView(FormView):
    template_name = 'sell_time/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

def manual_logout(request):
    logout(request)
    return redirect('homepage')

@login_required
def create_timepackage(request):
    price = None
    if request.method == 'POST':
        form = TimePackageForm(request.POST)
        if form.is_valid():
            timepackage = form.save(commit=False)
            timepackage.price = timepackage.duration_minutes * 1
            price = timepackage.price
            timepackage.creator = request.user
            timepackage.save()
            return redirect('my_timepackages')
    else:
        form = TimePackageForm()
    return render(request, 'sell_time/create_timepackage.html', {
        'form': form,
        'price': price
    })

@login_required
def my_timepackages(request):
    packages = TimePackage.objects.filter(creator=request.user)
    return render(request, 'sell_time/my_timepackages.html', {'packages': packages})



def product_list(request):
    if request.method == 'POST':
        duration = request.POST.get('duration')
        use_type = request.POST.get('use_type')            
        try:
            package = TimePackage.objects.get(duration_minutes = duration, use_type = use_type)
            cart = request.session.get('cart', [])
            cart.append({
                'id': package.id,
                'name': package.name,
                'duration': package.duration_minutes,
                'price': float(package.price)
            })
            request.session['cart'] = cart
            request.session.modified = True
        except:
            print("Sorry, invalid input. Please type a whole number.")
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

def cart(request):
    cart = request.session.get('cart', [])
    total = sum(item['price'] for item in cart)
    return render(request, 'sell_time/cart.html', {'cart': cart})

def clear_cart(request):
    request.session.pop('cart', None)
    return redirect('cart')

def pay(request):
    if request.method == 'POST':
        cart = request.session.get('cart', [])
        total = sum(item['price'] for item in cart)
        request.session['cart'] = []
        request.session.modified = True
        return render(request, 'sell_time/payment_success.html', {'total': total})
    return redirect('cart')



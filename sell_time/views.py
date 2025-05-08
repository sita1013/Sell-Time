from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Min 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.views.generic.edit import FormView
from django.views.decorators.http import require_http_methods, require_POST
from django.utils.timezone import now, timedelta
from .forms import TimePackageForm, CustomUserCreationForm
from .models import Purchase, TimePackage
from faker import Faker

def homepage(request):
    return render(request, 'sell_time/homepage.html')

class SignUpView(FormView):
    template_name = 'sell_time/signup.html'
    form_class = CustomUserCreationForm
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
        'price': price,
    })

@login_required
def my_timepackages(request):
    packages = TimePackage.objects.filter(creator=request.user)
    return render(request, 'sell_time/my_timepackages.html', {
        'packages': packages,
    })

def product_list(request):
    if request.method == 'POST':
        duration = request.POST.get('duration')
        use_type = request.POST.get('use_type')            
        try:
            duration = int(duration) 
            #added because future packages keep failing
            package = TimePackage.objects.get(duration_minutes = duration, use_type = use_type)
            cart = request.session.get('cart', [])
            cart.append({
                'id': package.id,
                'name': package.name,
                'duration': package.duration_minutes,
                'price': float(package.price),
            })
            request.session['cart'] = cart
            request.session.modified = True
        except:
            print("Sorry, something went wrong in production_list try block.")
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
    return render(request, 'sell_time/cart.html', {
        'cart': cart, 
        'total': total,
    })

def clear_cart(request):
    request.session.pop('cart', None)
    return redirect('cart')

def guest_checkout(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        cart = request.session.get('cart', [])
        if not email: 
            return render(request, 'sell_time/guest_checkout.html', {
                'error': 'Email is required to checkout as guest.',
                'cart': cart, 
                'total': sum(item['price'] for item in cart),
            })
        total = sum(item['price'] for item in cart)
        for item in cart: 
            Purchase.objects.create(
                user = None, 
                email = email, 
                package_id = item['id'],
                quantity = 1,
            )
        request.session['cart'] = []
        request.session.modified = True
        return render(request, 'sell_time/payment_success.html', {
            'guest_email': email,
            'total' : total,
        })
    cart = request.session.get('cart', [])
    total = sum(item['price'] for item in cart)
    return render(request, 'sell_time/guest_checkout.html', {
        'cart': cart,
        'total': total,
    })

@login_required
@require_http_methods(["GET", "POST"])
def user_checkout(request):
    cart = request.session.get('cart', [])
    total = sum(item['price'] for item in cart)
    if request.method == "POST":
        for item in cart: 
            Purchase.objects.create(
                user=request.user, 
                email = request.user.email,
                package_id = item['id'],
                quantity = 1,
            )
        #request.session['last_payment_total'] = total
        request.session['cart'] = []
        request.session.modified = True
        return render(request, 'sell_time/user_pay_success.html', {
            'total': total,
        })
    return render(request, 'sell_time/user_checkout.html', {
        'cart': cart, 
        'total': total,
    })

@login_required
def user_pay_success(request):
    total = request.session.get('last_payment_total', 0)
    return render(request, 'sell_time/user_pay_success.html', {'total': total})

@require_POST
@login_required
def send_to_bank(request):
    #send money to bank
    messages.success(request, "Funds will be transferred to your bank account.")
    return redirect('purchase_history')

@require_POST
@login_required
def store_credit(request):
    #store credit to user's account
    messages.success(request, "Amount stored as credit on your account.")
    return redirect('purchase_history')

@login_required
def purchase_history(request):
    user = request.user
    #all purchases where the user was indeed the user
    purchases = Purchase.objects.filter(user=user).select_related('package').order_by('-timestamp')
    #all sales where user was indeed the user
    sales = TimePackage.objects.filter(creator=user).order_by('-id')
    return render(request, 'sell_time/purchase_history.html', {
        'purchases': purchases,
        'sales': sales,
    })

@login_required
def user_purchase_graphs(request):
    user = request.user
    today = now().date()
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]

    purchases_by_day = []
    for day in last_7_days:
        count = Purchase.objects.filter(user=user, timestamp__date=day).count()
        purchases_by_day.append({'date': day.strftime('%Y-%m-%d'), 'count': count})

    labels = [entry['date'] for entry in purchases_by_day]
    counts = [entry['count'] for entry in purchases_by_day]

    return render(request, 'sell_time/user_purchase_graphs.html', {
        'labels': labels,
        'counts': counts
    })

def pay(request):
    if request.method == 'POST':
        cart = request.session.get('cart', [])
        total = sum(item['price'] for item in cart)
        request.session['cart'] = []
        request.session.modified = True
        return render(request, 'sell_time/payment_success.html', {'total': total})
    return redirect('cart')



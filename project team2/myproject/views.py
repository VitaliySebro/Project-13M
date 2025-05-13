from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout

def home(request):
    return render(request, 'home.html', {'MEDIA_URL': settings.MEDIA_URL})

def catalog_view(request):
    products = Product.objects.all()
    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(name__icontains=query)

    context = {'products': products, 'query': query}
    return render(request, 'catalog.html', context)

def product_list(request):
    products = Product.objects.all()
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    context = {'products': products}
    return render(request, 'your_template.html', context)

def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_sum = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total_price = product.price * quantity
        total_sum += total_price
        cart_items.append({
            'name': product.name,
            'quantity': quantity,
            'total_price': total_price,
        })

    return render(request, "cart.html", {
        "cart_items": cart_items,
        "total_sum": total_sum
    })

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart
    return redirect('catalog')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('home')  
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def reviews_view(request):
    reviews = request.session.get("reviews", [])

    if request.method == "POST":
        text = request.POST.get("text")
        if text:
            new_review = {"name": request.user.username, "text": text}
            reviews.insert(0, new_review)
            request.session["reviews"] = reviews
            return redirect("reviews")

    return render(request, "reviews.html", {"reviews": reviews})

def logout_view(request):
    logout(request)
    return redirect('reviews')
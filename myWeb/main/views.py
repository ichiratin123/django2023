from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from .models import Product,Cart,CartDetail,Review,Checkout
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm,CreateUserForm,ChangePasswordForm,CustomPasswordResetForm, CustomSetPasswordForm,ReviewForm,CheckoutForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView,PasswordChangeDoneView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy



def welcome(request):
    return render(request,'welcome.html')

def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'index.html', context)

def detail(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        cart = Cart.objects.filter(user=request.user, details__product=product).exists()
        reviews = Review.objects.filter(product=product)
        review_form = ReviewForm()

        if request.method == 'POST':
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.product = product
                review.save()
                return redirect('detail', pk=product.pk)

        context = {
            'product': product,
            'in_cart': cart,
            'reviews': reviews,
            'review_form': review_form,
        }
        return render(request, 'detail.html', context)
    else:
        return render(request, 'warn.html')

def warning(request):
    return render(request, 'warn.html')

def review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = Review.objects.filter(product=product)
    review_form = ReviewForm()

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('detail', pk=product.pk)

    context = {
        'product': product,
        'reviews': reviews,
        'review_form': review_form,
    }
    return render(request, 'review.html', context)

def about(request):
    return render(request, 'about.html')
    
def logout_user(request):
    logout(request)
    return redirect('mainhome')

def login_user(request):
    login(request)
    return redirect('index')

def signup(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CreateUserForm()
    return render(request, 'signup.html', {'form': form})


class ChangePasswordView(PasswordChangeView):
    template_name = 'passchange.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('passdone')

class change_password_done(PasswordChangeDoneView):
    template_name = 'passdone.html'

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'forgotpass.html'

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'forgotpassdone.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'passresetconf.html'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'passresetcomp.html'


@login_required
def addtocart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        cart, created = Cart.objects.get_or_create(user=request.user)
        try:
            cart_detail = CartDetail.objects.get(cart=cart, product=product)
            cart_detail.quantity += 1
            cart_detail.save()
        except CartDetail.DoesNotExist:
            cart_detail = CartDetail(cart=cart, product=product, quantity=1)
            cart_detail.save()
    return redirect('detail', pk=product.id)

def cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cartdetail = CartDetail.objects.filter(cart=cart)
        carttotal = cart.get_total_cost()

    except Cart.DoesNotExist:
        cartdetail = None
        carttotal = 0

    return render(request, 'cart.html', {
        'cartdetail': cartdetail,
        'carttotal': carttotal,
    })


@login_required
def removefromcart(request, pk):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_detail = CartDetail.objects.get(pk=pk)
        cart_detail.delete()
    except Cart.DoesNotExist or CartDetail.DoesNotExist:
        return redirect('cart')
    return redirect('cart')

@login_required
def clearcart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart.delete()
    except Cart.DoesNotExist or CartDetail.DoesNotExist:
        return redirect('cart')
    return redirect('cart')

def profile(request):
    return render(request,'profile.html')

def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    checkout_instance = Checkout.objects.filter(cart=cart).first()
    total_cost = cart.get_total_cost()

    if request.method == 'POST':
        form = CheckoutForm(request.POST, instance=checkout_instance)
        if form.is_valid():
            checkout = form.save(commit=False)
            checkout.cart = cart
            checkout.save()

            return redirect('checkoutsucc', pk=checkout.pk)

    else:
        form = CheckoutForm(instance=checkout_instance)

    return render(request, 'checkout.html', {'form': form, 'total_cost': total_cost})

def checkout_success(request, pk):
    cart = get_object_or_404(Cart, user=request.user)
    checkout = get_object_or_404(Checkout, pk=pk)
    total_cost = checkout.cart.get_total_cost()
    cart.details.all().delete()
    return render(request, 'checkoutsucc.html', {'checkout': checkout, 'total_cost': total_cost})
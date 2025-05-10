from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django.db.models import Q
import json
from cart.cart import Cart


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
            messages.success(request, 'You  have been Logged In')
            return redirect('home')
        else:
            messages.success(request, 'There was an error, Please try again')
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been Logged Out....')
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have Registered Successfully, Please Fill in your Profile Info")
            return redirect("update_info")
        else:
            messages.error(request, "Whoops! There was a problem, Please try again.")
            return redirect("register")
    else:
        return render(request, "register.html", {'form': form})

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def category(request, cat):
    cat = cat.replace("-", "")
    try:
        category = Category.objects.get(name=cat)
        products = Product.objects.filter(category=category)
        return render(request, "category.html", {"category": category, "products": products})
    except:
        messages.success(request, "That Category doesn't exist")
        return redirect("home")

def category_summary(request):
    categories = Category.objects.all()
    return render(request, "category_summary.html", {"categories": categories})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Your Profile has been updated successfully")
            return redirect("home")
        return render(request, "update_user.html", {"user_form": user_form})
    else:
        messages.error(request, "You need to be logged in to update your profile")
        return redirect("login")

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        form = ChangePasswordForm(current_user, request.POST)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Your Password has been updated successfully, Please Log In Again")
                login(request, current_user)
                return redirect("home")
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect("update_password")
        else:
            return render(request, "update_password.html", {"form": form})
    else:
        messages.error(request, "You need to be logged in to update your profile")
        return redirect("login")


def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Profile has been updated successfully")
            return redirect("home")
        return render(request, "update_info.html", {"form": form})
    else:
        messages.error(request, "You need to be logged in to update your profile")
        return redirect("login")

def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        searched_products = Product.objects.filter(Q(name__icontains=searched) |Q(description__icontains=searched))
        if not searched_products:
            messages.error(request, "No products found matching your search. Please try again.")
            return render(request, "search.html", {})
        else:
            messages.success(request, f"Found {searched_products.count()} product(s) matching your search.")
            return render(request, "search.html", {'searched_products': searched_products})
    else:
        return render(request, "search.html", {})
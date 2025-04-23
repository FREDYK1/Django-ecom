from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm
from django import forms


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
            messages.success(request, "You have Registered Successfully, Welcome")
            return redirect("home")
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
        if request.method == "POST" and user_form.is_valid():
            user_form.save()
            messages.success(request, "Your Profile has been updated successfully")
            return redirect("update_user")
        return render(request, "update_user.html", {"user_form": user_form})
    else:
        messages.error(request, "You need to be logged in to update your profile")
        return redirect("login")
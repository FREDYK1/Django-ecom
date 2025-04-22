from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .cart import Cart
from store.models import Product
from typing import Any
from django.contrib import messages


def cart_summary(request: Any) -> Any:
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_products": cart_products, "quantities": quantities, "total": totals})


def cart_add(request: Any) -> JsonResponse:
    cart = Cart(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        product_qty = int(request.POST.get("product_qty"))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=product_qty)
        cart_quantity = cart.__len__()
        messages.success(request, "Item Added to Cart")
        return JsonResponse({"qty": cart_quantity})
    return JsonResponse({"error": "Invalid request"}, status=400)


def cart_delete(request: Any) -> JsonResponse:
    cart = Cart(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        cart.delete(product=product_id)
        product = Product.objects.get(id=product_id)
        messages.success(request, f"{product} was successfully deleted")
        return JsonResponse({"product": product_id})
    return JsonResponse({"error": "Invalid request"}, status=400)


def cart_update(request: Any) -> JsonResponse:
    cart = Cart(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        product_qty = int(request.POST.get("product_qty"))
        cart.update(product=product_id, quantity=product_qty)
        product = Product.objects.get(id=product_id)
        messages.success(request, f"{product} was successfully updated")
        return JsonResponse({"qty": product_qty})
    return JsonResponse({"error": "Invalid request"}, status=400)
from django.shortcuts import render, redirect
from .models import Order, Product

def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)

def purchase(request):
    if request.method=="POST":
        
        product = Product.objects.get(id=request.POST['product_id'])

        quantity_from_form = int(request.POST["quantity"])
        price = float(product.price)
        total_charge = quantity_from_form * price
        print("Charging credit card...")
        new_order = Order.objects.create(quantity_ordered=quantity_from_form, total_price=total_charge)

        return redirect(f'/checkout')

    return redirect('/')

def checkout(request):
    total_item_count = 0
    total_spent = 0

    order = Order.objects.last()
    quantity = order.quantity_ordered
    total = order.total_price

    for order in Order.objects.all():
        total_item_count += order.quantity_ordered
        
        total_spent += order.total_price

    context = {
        "quantity": quantity,
        "new_charge": total,
        "total_items": total_item_count,
        "total_money_spent": total_spent
    }
    
    return render(request, "store/checkout.html", context)
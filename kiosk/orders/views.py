from django.shortcuts import render, redirect,  get_object_or_404
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem
from .models import Order , Payment, OrderProduct
import datetime 
from .forms import OrderForm
import json

from django.contrib.auth.decorators import login_required   
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string 

# Create your views here.

#payments

def payments(request):
   body = json.loads(request.body)
   order = Order.objects.get(user=request.user, is_ordered=False, order_number=body["orderID"])
   #store transaction details inside payment model
   payment = Payment(
      user = request.user, 
      payment_id = body["transID"],
      payment_method = body["payment_method"],
      amount_paid = order.order_total,
      status = body["status"],
   )
   payment.save()

   #update order model
   order.payment = payment
   order.is_ordered = True
   order.save()

   #Move the cart items to order products table
   cart_items = CartItem.objects.filter(user=request.user)

   for item in cart_items:
      orderproduct =OrderProduct()
      orderproduct.order_id = order.id
      orderproduct.payment = payment
      orderproduct.user_id = request.user.id
      orderproduct.product_id = item.product.id
      orderproduct.quantity = item.quantity
      orderproduct.product_price = item.product.price
      orderproduct.ordered = True
      orderproduct.save()

      cart_item = CartItem.objects.get(id=item.id)
      product_variation = cart_item.variations.all()
      orderproduct = OrderProduct.objects.get(id=orderproduct.id)
      orderproduct.variation.set(product_variation)
      orderproduct.save()
        
    #Reduce the quantity of sold products
      product =Product.objects.get(id=item.product_id)
      product.stock -= item.quantity
      product.save()
   
   
    #Clear the cart
   CartItem.objects.filter(user=request.user).delete()
   
   #Send order received email to customer
   mail_subject = "Thank you for shopping at Online Furniture Shop .Your house decorating shop."
   message = render_to_string("orders/order_received.html", {
                'user': request.user,
                'order': order,
                 })
   to_email = request.user.email
   send_email = EmailMessage(mail_subject, message, to=[to_email])
   send_email.send()
   #Send order number and transaction id back sendData method via json response
   data = {
      "order_number": order.order_number,
      'transID': payment.payment_id
   }
   return JsonResponse(data)


#place order
def place_order(request, total=0, quantity = 0):
   current_user = request.user

   # if cart count is less than or equal to zero then redirect back to store

   cart_items = CartItem.objects.filter(user=current_user)
   cart_count = cart_items.count()
   if cart_count <= 0 :
      return redirect('store')
   
   grand_total = 0
   total=0
   

   for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
   tax = (2 * total)/100
   grand_total = total + tax 
              

   if request.method == 'POST':
      form = OrderForm(request.POST)
      if form.is_valid():
         # store billing in the order table
        
        data = Order()
        data.user = current_user
        data.first_name = form.cleaned_data["first_name"]
        data.last_name = form.cleaned_data["last_name"]
        data.phone = form.cleaned_data["phone"]
        data.email = form.cleaned_data["email"]
        data.address_line_1 = form.cleaned_data["address_line_1"]
        data.address_line_2 = form.cleaned_data["address_line_2"]
        data.country = form.cleaned_data["country"]
        data.state = form.cleaned_data["state"]
        data.city = form.cleaned_data["city"]
        data.order_note = form.cleaned_data["order_note"]
        data.order_total = grand_total
        data.tax = tax
        data.ip = request.META.get('REMOTE_ADDR')
        data.save()
        #Generate OrderNumbher
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr, mt , dt)
        current_date = d.strftime("%Y%m%d")
        order_number = current_date + str(data.id)
        data.order_number = order_number
        data.save()

        order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
        context = {
           'order': order,
           'cart_items': cart_items,
           'total': total,
           'tax': tax,
           'grand_total': grand_total, 
        }
        return render(request, 'orders/payments.html', context)
      else:
      #   print(form.errors)  # Print the form errors for debugging purposes
        return HttpResponse("Invalid form data")
      
   else:
        return redirect("checkout")
   
   
def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
   #  print("order_number->", order_number)
   #  print("transID ->", transID)
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)
        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)
    except(Payment.DoesNotExist,  Order.DoesNotExist):
     return redirect('home')




def order_products(request):
   ordered_products = OrderProduct.objects.all()
   context = {
    "ordered_products": ordered_products,
   }

   return render(request, "orders/ordered_products.html", context)


def all_orders(request):
   orders_list = Order.objects.all()
   context = {
    "orders_list": orders_list,
   }


   return render(request, "orders/orders.html ", context)


def all_payments(request):
   payments = Order.objects.all()
   context = {
    "payments": payments,
   }


   return render(request, "orders/all_payments.html ", context)


@login_required(login_url='login')
def order_details(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity
    
    if order.status not in ['Completed', 'Cancelled']:
        order.status = 'Received'
        order.save()
    can_mark_completed = order.status not in ['Completed', 'Cancelled']
    can_mark_dispatched = order.status not in  ['Completed', 'Cancelled', 'Pending']

    if request.method == 'POST':
         if 'mark_completed' in request.POST and can_mark_completed:
            order.mark_completed()
         elif 'mark_dispatched' in request.POST and can_mark_dispatched:
            order.mark_dispatched()
         return redirect('orders_list')
                       
    context = {
        "order_detail": order_detail,
        "order": order,
        "subtotal": subtotal,
         "can_mark_completed": can_mark_completed,
         "can_mark_dispatched": can_mark_dispatched,
    }
       
   
    return render(request, "orders/order_details.html", context)


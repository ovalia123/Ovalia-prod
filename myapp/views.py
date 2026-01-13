from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect, render

from gestion.models import *
import stripe
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import traceback
from decimal import Decimal
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY

TPS_RATE = Decimal("0.05")
TVQ_RATE = Decimal("0.09975")

def index(request):
    latest_products = Sales.objects.filter(available=True).order_by('-created')[:3]
    context = {'latest_products': latest_products}
    return render(request, 'user/index.html', context)


def faq(request):
    return render(request, 'user/faq.html')


def condition(request):
    return render(request, 'Conditions_utilisation.html')


def service(request):
    return render(request, 'user/service.html')


def event(request):
    return render(request, 'user/event.html')


def contact(request):
    return render(request, 'user/contact.html')


def logout_view(request):
    logout(request)
    return redirect('index')


def login(request):
    return render(request, 'user/login.html')


def member(request):
    return render(request, 'user/members.html')


def shop(request):
    return render(request, 'user/shop/shop.html')


def shop_14k(request):
    products = Product.objects.filter(available=True, materiaux='Or massif 14k')
    print(products)
    return render(request, 'user/shop/or_massif.html', {'products': products})


def shop_10k(request):
    products = Product.objects.filter(available=True, materiaux='Or massif 10k')
    return render(request, 'user/shop/or_massif_10k.html', {'products': products})


def shop_rempli(request):
    products = Product.objects.filter(available=True, materiaux='Or rempli')
    return render(request, 'user/shop/or_rempli.html', {'products': products})


def shop_argent(request):
    products = Product.objects.filter(available=True, materiaux='Argent sterling')
    return render(request, 'user/shop/argent.html', {'products': products})


def charms(request):
    return render(request, 'user/shop/charms.html')


def boutique(request):
    sales = Sales.objects.filter(available=True).order_by('-created')
    context = {'sales': sales}
    return render(request, 'user/sales/boutique.html', context)


def sale_detail(request, sale_id):
    sale = get_object_or_404(Sales, id=sale_id, available=True)
    return render(request, 'user/sales/sale_detail.html', {'sale': sale})


def _get_cart(request):
    return request.session.setdefault('cart', {})


def _cart_items_with_totals(request):
    cart = _get_cart(request)
    sales = Sales.objects.filter(id__in=cart.keys())
    items = []
    total = Decimal('0.00')
    for sale in sales:
        quantity = int(cart.get(str(sale.id), 0))
        subtotal = sale.price * quantity
        total += subtotal
        items.append({'sale': sale, 'quantity': quantity, 'subtotal': subtotal})
    return items, total


def add_to_cart(request, sale_id):
    sale = get_object_or_404(Sales, id=sale_id, available=True)
    cart = _get_cart(request)
    cart[str(sale_id)] = cart.get(str(sale_id), 0) + 1
    request.session.modified = True
    messages.success(request, f"{sale.name} a été ajouté à votre panier.")
    return redirect('boutique')


def update_cart(request, sale_id):
    sale = get_object_or_404(Sales, id=sale_id, available=True)
    cart = _get_cart(request)
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 1
    if quantity > 0:
        cart[str(sale_id)] = quantity
        messages.info(request, f"Quantité mise à jour pour {sale.name}.")
    else:
        cart.pop(str(sale_id), None)
        messages.info(request, f"{sale.name} a été retiré du panier.")
    request.session.modified = True
    return redirect('cart')


def remove_from_cart(request, sale_id):
    sale = get_object_or_404(Sales, id=sale_id, available=True)
    cart = _get_cart(request)
    cart.pop(str(sale_id), None)
    request.session.modified = True
    messages.info(request, f"{sale.name} a été retiré du panier.")
    return redirect('cart')


def cart(request):
    items, total = _cart_items_with_totals(request)
    return render(request, 'user/sales/cart.html', {'cart_items': items, 'total': total})



def checkout(request):
    items, total = _cart_items_with_totals(request)

    if not items:
        return redirect('cart')

    return render(request, 'user/sales/checkout.html', {
        'cart_items': items,
        'total': total,
    })





def create_checkout_session(request):
    items, total = _cart_items_with_totals(request)

    if not items:
        return redirect('cart')

    line_items = []

    for item in items:
        sale = item["sale"]
        line_items.append({
            "price_data": {
                "currency": "cad",
                "product_data": {
                    "name": sale.name,
                },
                "unit_amount": int(sale.price * 100),
            },
            "quantity": item["quantity"],
        })

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=request.build_absolute_uri(
            reverse("checkout_success")
        ),
        cancel_url=request.build_absolute_uri(
            reverse("checkout_cancel")
        ),
    )

    return redirect(session.url)


def checkout_success(request):
    request.session["cart"] = {}
    request.session.modified = True
    return render(request, "user/sales/checkout_success.html")


def checkout_cancel(request):
    return render(request, "user/sales/checkout_cancel.html")



def create_checkout_session(request):
    cart = request.session.get("cart", {})
    if not cart:
        return redirect("cart")

    # 🔹 CUSTOMER INFO FROM FORM
    customer_data = {
        "first_name": request.POST.get("first_name"),
        "last_name": request.POST.get("last_name"),
        "email": request.POST.get("email"),
        "phone": request.POST.get("phone"),
        "address": request.POST.get("address"),
        "city": request.POST.get("city"),
        "postal_code": request.POST.get("postal_code"),
        "country": request.POST.get("country"),
    }

    line_items = []
    metadata = customer_data.copy()

    sales = Sales.objects.filter(id__in=cart.keys())

    # ---- CALCULATE SUBTOTAL ----
    subtotal = Decimal("0.00")

    for sale in sales:
        quantity = int(cart[str(sale.id)])
        subtotal += sale.price * quantity

        line_items.append({
            "price_data": {
                "currency": "cad",
                "product_data": {
                    "name": sale.name,
                },
                "unit_amount": int(sale.price * 100),
            },
            "quantity": quantity,
        })

        metadata[f"sale_{sale.id}"] = quantity

    # ---- CALCULATE TAXES ----
    tps = (subtotal * TPS_RATE).quantize(Decimal("0.01"))
    tvq = (subtotal * TVQ_RATE).quantize(Decimal("0.01"))
    total_taxes = tps + tvq

    # Store taxes in metadata (for webhook / Order)
    metadata["tps"] = str(tps)
    metadata["tvq"] = str(tvq)

    # ---- ADD TAX LINE ITEM ----
    if total_taxes > 0:
        line_items.append({
            "price_data": {
                "currency": "cad",
                "product_data": {
                    "name": "Taxes (TPS + TVQ)",
                },
                "unit_amount": int(total_taxes * 100),
            },
            "quantity": 1,
        })

    # ---- CREATE STRIPE SESSION ----
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        customer_email=customer_data["email"],
        metadata=metadata,
        success_url=request.build_absolute_uri(
            reverse("checkout_success")
        ),
        cancel_url=request.build_absolute_uri(
            reverse("checkout_cancel")
        ),
    )

    return redirect(session.url)

@csrf_exempt
def stripe_webhook(request):
    print("\n=== STRIPE WEBHOOK HIT ===")

    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        print("❌ Signature verification failed:", repr(e))
        return HttpResponse(status=400)

    event_type = event.get("type")
    print("Event type:", event_type)

    # We only care about completed checkouts
    if event_type != "checkout.session.completed":
        print("Ignoring event:", event_type)
        return HttpResponse(status=200)

    try:
        session = event["data"]["object"]
        print("Checkout session id:", session["id"])

        metadata = session.get("metadata") or {}
        print("Session metadata:", metadata)

        # Idempotency
        if Order.objects.filter(stripe_session_id=session["id"]).exists():
            print("⚠️ Order already exists for session:", session["id"])
            return HttpResponse(status=200)

        # ---- CREATE ORDER (ONLY FROM METADATA) ----
        order = Order.objects.create(
            email=metadata.get("email", ""),
            phone=metadata.get("phone", ""),
            first_name=metadata.get("first_name", "Stripe"),
            last_name=metadata.get("last_name", "Customer"),
            address=metadata.get("address", ""),
            city=metadata.get("city", ""),
            postal_code=metadata.get("postal_code", ""),
            country=metadata.get("country", "Canada"),
            total=Decimal(session.get("amount_total", 0)) / 100,
            stripe_session_id=session["id"],
            paid=True,
        )

        print("✅ Order created:", order.id)

        # ---- CREATE ORDER ITEMS ----
        for key, quantity in metadata.items():
            if not key.startswith("sale_"):
                continue

            sale_id = key.replace("sale_", "")
            print("Creating OrderItem | sale:", sale_id, "| qty:", quantity)

            sale = Sales.objects.get(id=int(sale_id))
            OrderItem.objects.create(
                order=order,
                sale=sale,
                quantity=int(quantity),
                price=sale.price,
            )

        print("✅ Order items created")
        print("✅ checkout.session.completed handled successfully")
        return HttpResponse(status=200)

    except Exception as e:
        print("❌ ERROR while processing checkout.session.completed:", repr(e))
        traceback.print_exc()
        # Return 200 to prevent Stripe retries while debugging
        return HttpResponse(status=200)
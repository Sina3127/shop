from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.utils.translation import gettext as _
from django.views import generic

from shop.form import AddReview, AddTransaction
from shop.models import Banner, Transaction, TransactionItem
from shop.models import Product, Cart, Category, ReviewComment, CartItem


# class Home(generic.TemplateView):
#     template_name = 'shop/home.html'


def Home(request):
    page = loader.get_template('shop/home.html')
    recom = None
    tag = request.GET.get('tag', None)
    if tag is not None:
        recom = Product.objects.filter(tag=tag).all()
    else:
        recom = Product.objects.all()
    context = {
        'products': recom,
        'categories': Category.objects.filter(parent__isnull=True).all(),
        'banner': Banner.objects.filter(is_active=True).order_by('number').all(),
    }
    return HttpResponse(page.render(context, request))


def itemDetails(request,
                id):  # price, title, list(pictures), copon, review, decription, remaining, you may also like, size,
    product = get_object_or_404(Product, id=id)
    context = {
        'product': product,
        'categories': Category.objects.filter(parent__isnull=True).all(),
    }
    return render(request, 'shop/itemDetails.html', context)


def CartDetails(request):
    if request.user.is_authenticated:
        page = loader.get_template('shop/cart.html')
        cart, created = Cart.objects.get_or_create(user=request.user)

        context = {
            'cart': cart,
            't_amount': cart.t_price()
        }
        return HttpResponse(page.render(context, request))
    else:
        return redirect('signup')


def addToCart(request):  # cart, you may also like,
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        id = int(request.POST.get('id')[0])
        product = get_object_or_404(Product, id=id)
        if CartItem.objects.filter(cart=cart, product=id).exists():
            cart_item = CartItem.objects.filter(cart=cart, product=product).first()
            cart_item.count += 1
            cart_item.save()
        else:
            CartItem.objects.create(cart=cart, product=product, count=1)

        if CartItem.objects.get(cart=cart, product=id).count > product.inventory:
            messages.add_message(request, messages.WARNING, _("sorry, we don't have enough product!"))
            CartItem.objects.filter(cart=cart, product=id).update(count=product.inventory)
        else:
            messages.add_message(request, messages.INFO, _("new product added"))
        return redirect('cart')
    else:
        return redirect('signup')


def removeFromCart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.POST.get('id')
        id = int(product_id[0])
        if CartItem.objects.filter(cart=cart, product=id).exists():
            cart_item = CartItem.objects.filter(cart=cart, product=id).first()
            cart_item.count -= 1
            if cart_item.count < 1:
                CartItem.objects.filter(id=cart_item.id).delete()
            else:
                cart_item.save()
        return redirect('cart')
    else:
        return redirect('signup')


def orderSumary(request):  # previes card,
    return HttpResponse("orderSumary")


def items(request):  # special offers, itemDetails
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'shop/items.html', context)


def Categories(request, id):  # list of chategories
    category = get_object_or_404(Category, pk=id)
    childCategories = Category.objects.filter(parent=category).all()
    context = {
        'category': category,
        'childCategories': childCategories,
    }
    return render(request, 'shop/categories.html', context)


def CategoriesDetials(request, id):
    category = get_object_or_404(Category, pk=id)
    product = Product.objects.filter(category=category).all()
    context = {
        'category': category,
        'products': product,
    }
    return render(request, 'shop/categories-details.html', context)


def orderStatus(request):  # locations, arrival, itemdetails,
    return HttpResponse("orderStatus")


def searchbar(request):
    if request.method == "GET":
        search = request.GET.get('search')
        products = Product.objects.filter(title__contains=search).all()
        return render(request, 'shop/searchbar.html', {'products': products})


def reviewings(request, id):  # itemdetails
    product = get_object_or_404(Product, id=id)
    form = None
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddReview(request.POST)
            if form.is_valid():
                text = form.cleaned_data.get('text')
                points = form.cleaned_data.get('point')
                user = request.user
                ReviewComment(user=user, text=text, point=points, review=product).save()
                form = AddReview()
        else:
            form = AddReview()
    context = {
        'product': product,
        'form': form,
    }
    return render(request, 'shop/reviewings.html', context)


def shipping(request):
    if not request.user.is_authenticated:
        return redirect('signup')

    if request.method == 'POST':
        form = AddTransaction(request.user, request.POST, request.FILES)
        if form.is_valid():
            address = form.cleaned_data.get('address')
            send_time = form.cleaned_data.get("send_time")
            user = request.user
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart).all()
            with transaction.atomic():
                t = Transaction.objects.create(user=user, state_payment=Transaction.STATE.NEW,
                                               send_time=send_time, address=address,
                                               shipping_price=settings.SHIPPING_PRICE,
                                               total_price=cart.t_price()
                                               )
                for cart_item in cart_items:
                    TransactionItem.objects.create(
                        product=cart_item.product,
                        transaction=t,
                        count=cart_item.count,
                        price=cart_item.product.price,
                    )

            return redirect('payment')
    else:
        form = AddTransaction(request.user)
    return render(request, 'shop/shipping.html', {'form': form})


class PaymentView(generic.TemplateView):
    template_name = 'shop/payment.html'

    def get(self, request, *args, **kwargs):
        t = Transaction.objects.filter(user=self.request.user).last()
        t.state_payment = Transaction.STATE.PENDING
        t.save()
        return super(PaymentView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs = super(PaymentView, self).get_context_data(**kwargs)
        t = Transaction.objects.filter(user=self.request.user).last()
        transaction_item = TransactionItem.objects.filter(transaction=t).all()
        products = Product.objects.filter(id__in=[i.product_id for i in transaction_item]).all()
        kwargs["transaction"] = t
        kwargs["transaction_item"] = transaction_item
        kwargs["products"] = products
        return kwargs

    def post(self, request, *args, **kwargs):
        CartItem.objects.filter(cart=self.request.user.cart).delete()
        t = Transaction.objects.filter(user=self.request.user).last()
        t.state_payment = Transaction.STATE.PAYMENT_APPROVED
        t.save()
        return redirect('home')

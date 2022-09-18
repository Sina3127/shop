from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.views import generic


# class Home(generic.TemplateView):
#     template_name = 'shop/home.html'
from django.views.decorators.cache import cache_page

from shop.form import AddReview
from shop.models import Product, Cart, Category, ReviewComment


@cache_page(60 * 10)
def Home(request):
    page = loader.get_template('shop/home.html')
    recom = None
    tag = request.GET.get('tag', None)
    if tag is not None:
        recom = Product.objects.filter(tag=tag).all()
    else:
        recom = Product.objects.all()
    context = {
        'recom' : recom
    }
    return HttpResponse(page.render(context, request))


def itemDetails(request, id):  # price, title, list(pictures), copon, review, decription, remaining, you may also like, size,
    product = get_object_or_404(Product, id=id)
    context = {
        'product' : product
    }
    return render(request, 'shop/itemDetails.html', context)


def CartDetails(request):
    if request.user.is_authenticated:
       page = loader.get_template('shop/cart.html')
       # cart = Cart.objects.filter(user=request.user).all()
       cart, created = Cart.objects.get_or_create(user=request.user)
       context = {
           'cart' : cart
       }
       return HttpResponse(page.render(context, request))
    else:
        return redirect('signup')

def addToCart(request):  # cart, you may also like,
    print(request.POST)
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.POST.get('id')
        id = int(product_id[0])
        cart.products.add(id)
        return redirect('cart')
    else:
        return redirect('signup')

def removeFromCart(request):  # cart, you may also like,
    return HttpResponse("removeFromCart")


def orderSumary(request):  # previes card,
    return HttpResponse("orderSumary")


def payment(request):  # cart, amount of money, all card numbers, all locations
    return HttpResponse("payment")


def items(request):  # special offers, itemDetails
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'shop/items.html', context)

def Categories(request):  # list of chategories
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'shop/categories.html', context)

def orderStatus(request):  # locations, arrival, itemdetails,
    return HttpResponse("orderStatus")


def search(request):  # search word, items,
    return HttpResponse("search")


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
        'product' : product,
        'form' : form,
    }
    return render(request, 'shop/reviewings.html', context)
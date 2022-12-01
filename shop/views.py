from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader

from shop.form import AddReview
from shop.models import Banner
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
        # cart = Cart.objects.filter(user=request.user).all()
        cart, created = Cart.objects.get_or_create(user=request.user)

        t_amount = 0

        for c in cart.cart_items.all():
            amount = c.product.price * c.count
            t_amount += amount

        context = {
            'cart': cart,
            't_amount': t_amount
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
        if CartItem.objects.filter(cart=cart, product=id).exists():
            cart_item = CartItem.objects.filter(cart=cart, product=id).first()
            cart_item.count += 1
            cart_item.save()
        else:
            CartItem.objects.create(cart=cart, product_id=id, count=1)
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

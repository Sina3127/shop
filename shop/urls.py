from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.Home, name='home'),
    path('cart/', views.CartDetails,name='cart'),
    path('itemDetails/<int:id>/', views.itemDetails, name='itemDetails'),
    path('addToCart/', views.addToCart, name='addToCart'),
    path('removeFromCart/', views.removeFromCart, name='removeFromCart'),
    path('order-sumary/', views.orderSumary),
    path('payment/', views.payment),
    path('items/', views.items),
    path('categories/<int:id>', views.Categories, name='categories'),
    path('categories-details/<int:id>/', views.CategoriesDetials, name='categories-details'),
    path('orderStatus/', views.orderStatus),
    path('reviewings/<int:id>/', views.reviewings, name='reviewings'),
    path('searchbar/', views.searchbar, name='searchbar'),
    path('shipping/', views.shipping, name='shipping'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
]
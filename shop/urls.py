from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.Home, name='home'),
    path('cart/', views.CartDetails,name='cart'),
    path('itemDetails/<int:id>/', views.itemDetails, name='itemDetails'),
    path('addToCart/', views.addToCart, name='addToCart'),
    path('removeFromCart/', views.removeFromCart),
    path('order-sumary/', views.orderSumary),
    path('payment/', views.payment),
    path('items/', views.items),
    path('categories/', views.Categories, name='categories'),
    path('orderStatus/', views.orderStatus),
    path('search/', views.search),
    path('reviewings/<int:id>/', views.reviewings, name='reviewings')
]
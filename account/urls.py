from django.urls import path, include
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('changePassword/', views.changePassword),
    path('addlocation/', views.addLocation,  name='add_location'),
    path('add_phone_number/', views.addPhoneNumber,  name='add_phone_number'),
    path('removeLocation/', views.removeLocation,),
    path('', include('django.contrib.auth.urls')),
]
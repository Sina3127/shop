from django.urls import path, include

from . import views
from .views import LogInView

urlpatterns = [
    path('login/', LogInView.as_view(), name='login'),
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('changePassword/', views.changePassword),
    path('addlocation/', views.addLocation, name='add_location'),
    path('addPhoneNumber/', views.addPhoneNumber, name='addPhoneNumber'),
    path('removeLocation/<int:id>/', views.removeLocation, ),
    path('removePhoneNumber/<int:id>/', views.removePhoneNumber, ),
    path('logout/', views.LogOut.as_view(), name='logout'),
]

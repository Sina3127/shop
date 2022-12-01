from django.urls import path, include
from . import views

urlpatterns = [
    path('profile/', views.profile.as_view(), name='profile'),
    path('signup/', views.signup, name='signup'),
    path('changePassword/', views.changePassword),
    path('addlocation/', views.addLocation),
    path('removeLocation/', views.removeLocation),
    path('', include('django.contrib.auth.urls')),
]
"""
URL configuration for car_parking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from Car_Parking_administration import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('available/', views.available_parking_spots, name='available_parking_spots'),
    path('search/', views.search_parking_spots, name='search_parking_spots'),
    path('reserve/<int:spot_id>/', views.reserve_parking_spot, name='reserve_parking_spot'),
    path('reservations/', views.view_reservations, name='view_reservations'),
]

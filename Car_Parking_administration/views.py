from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import ParkingSpot, Reservation
from geopy.distance import geodesic

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

login = auth_views.LoginView.as_view(template_name='registration/login.html')

def available_parking_spots(request):
    parking_spots = ParkingSpot.objects.filter(available=True)
    context = {'parking_spots': parking_spots}
    return render(request, 'available_parking_spots.html', context)

def search_parking_spots(request):
    if request.method == 'POST':
        latitude = float(request.POST['latitude'])
        longitude = float(request.POST['longitude'])
        radius = float(request.POST['radius'])
        user_location = (latitude, longitude)
        parking_spots = ParkingSpot.objects.filter(available=True)
        nearby_parking_spots = []
        for spot in parking_spots:
            spot_location = (spot.latitude, spot.longitude)
            distance = geodesic(user_location, spot_location).meters
            if distance <= radius:
                nearby_parking_spots.append(spot)
        context = {'parking_spots': nearby_parking_spots}
        return render(request, 'search_results.html', context)
    else:
        return render(request, 'search_form.html')

def reserve_parking_spot(request, spot_id):
    if request.method == 'POST':
        hours = int(request.POST['hours'])
        parking_spot = ParkingSpot.objects.get(id=spot_id)
        price = hours * parking_spot.price_per_hour
        parking_spot.available = False
        parking_spot.save()
        reservation = Reservation(parking_spot=parking_spot, user=request.user, price=price)
        reservation.save()
        return render(request, 'reservation_confirmation.html', {'reservation': reservation})
    else:
        parking_spot = ParkingSpot.objects.get(id=spot_id)
        context = {'parking_spot': parking_spot}
        return render(request, 'reservation_form.html', context)

def view_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    context = {'reservations': reservations}
    return render(request, 'view_reservations.html', context)

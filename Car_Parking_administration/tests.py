from django.test import TestCase
from django.urls import reverse
from .models import ParkingSpot, Reservation
from django.contrib.auth import get_user_model

User = get_user_model()

class AvailableParkingSpotsViewTests(TestCase):
    def test_no_parking_spots(self):
        """
        If no parking spots are available, an appropriate message is displayed.
        """
        response = self.client.get(reverse('available_parking_spots'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No parking spots are available.")
        self.assertQuerysetEqual(response.context['parking_spots'], [])

    def test_some_parking_spots(self):
        """
        If some parking spots are available, they are displayed.
        """
        ParkingSpot.objects.create(latitude=37.8716, longitude=-122.2727, available=True)
        response = self.client.get(reverse('available_parking_spots'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['parking_spots'],
            ['<ParkingSpot: ParkingSpot object (1)>']
        )

class SearchParkingSpotsViewTests(TestCase):
    def test_search_form(self):
        """
        The search form is displayed.
        """
        response = self.client.get(reverse('search_parking_spots'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Search for Parking Spots")

    def test_search_results(self):
        """
        The search results are displayed.
        """
        ParkingSpot.objects.create(latitude=37.8716, longitude=-122.2727, available=True)
        data = {'latitude': '37.8716', 'longitude': '-122.2727', 'radius': '1000'}
        response = self.client.post(reverse('search_parking_spots'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Search Results")
        self.assertQuerysetEqual(
            response.context['parking_spots'],
            ['<ParkingSpot: ParkingSpot object (1)>']
        )

class ReserveParkingSpotViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
    
    def test_reservation_form(self):
        """
        The reservation form is displayed.
        """
        spot = ParkingSpot.objects.create(latitude=37.8716, longitude=-122.2727, available=True)
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('reserve_parking_spot', args=[spot.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reserve Parking Spot")

    def test_reservation_confirmation(self):
        """
        The reservation confirmation is displayed.
        """
        spot = ParkingSpot.objects.create(latitude=37.8716, longitude=-122.2727, available=True)
        

from datetime import timedelta

from django.contrib.gis.geos import Point
from django.db.models import Q
from django.utils import timezone
from rest_framework.test import APITestCase

from stadium.models import Stadium, StadiumBooking
from userprofile.models import UserProfile
from userprofile.models.userprofile import RoleChoices


class TestStadium(APITestCase):
    maxDiff = None

    @classmethod
    def setUpTestData(cls) -> None:
        cls.vendor = UserProfile.objects.create_user(username='vendor', password='vendor', role=RoleChoices.VENDOR)
        cls.user = UserProfile.objects.create_user(username='user', password='user', role=RoleChoices.USER)

        cls.stadium1 = Stadium.objects.create(
            vendor=cls.vendor, name='stadium1', address='address1', contact='contact1', price_per_hour=100.00,
            location=Point(80.123, 80.123)
        )
        cls.stadium2 = Stadium.objects.create(
            vendor=cls.vendor, name='stadium2', address='address2', contact='contact2', price_per_hour=200.00,
            location=Point(50.123, 50.123)
        )
        cls.stb1 = StadiumBooking.objects.create(
            stadium=cls.stadium1, user=cls.user, start_time='2021-01-01 10:00:00', end_time='2021-01-01 11:00:00'
        )
        cls.stb2 = StadiumBooking.objects.create(
            stadium=cls.stadium2, user=cls.user, start_time='2021-01-01 20:00:00', end_time='2021-01-01 21:00:00'
        )

        cls.post_data = {
            'name': 'stadium3', 'address': 'address3', 'contact': 'contact3', 'price_per_hour': 300.00,
            'lat': 30.123, 'lon': 30.123
        }
        cls.update_data = {
            'name': 'stadium3', 'address': 'address3', 'contact': 'contact3', 'price_per_hour': 300.00,
            'lat': 30.123, 'lon': 30.123
        }
        cls.detail_data = {
            'id': cls.stadium1.id, 'name': 'stadium1', 'address': 'address1', 'contact': 'contact1',
            'price_per_hour': '100.00', 'lat': 80.123, 'lon': 80.123
        }

        cls.create_read_url = '/api/v1/stadium/stadium/'
        cls.read_update_delete_url = f'/api/v1/stadium/stadium/{cls.stadium1.id}/'

    def setUp(self) -> None:
        self.client.force_authenticate(user=None)

    def test_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.create_read_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

        self.assertEqual(response.json()[0], self.detail_data)

    def test_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.read_update_delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.detail_data)

    def test_create(self):
        self.client.force_authenticate(user=self.vendor)
        response = self.client.post(self.create_read_url, self.post_data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Stadium.objects.filter(
            vendor=self.vendor, name='stadium3', address='address3', contact='contact3', price_per_hour=300.00,
        ).count(), 1)
        self.assertEqual(Stadium.objects.get(id=response.json()['id']).lat, 30.123)
        self.assertEqual(Stadium.objects.get(id=response.json()['id']).lon, 30.123)

    def test_create_required_fields(self):
        self.client.force_authenticate(user=self.vendor)
        response = self.client.post(self.create_read_url, {}, format='json')
        content = {
            'name': ['This field is required.'], 'address': ['This field is required.'],
            'contact': ['This field is required.'], 'price_per_hour': ['This field is required.'],
            'lat': ['This field is required.'], 'lon': ['This field is required.']
        }

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), content)

    def test_update(self):
        self.client.force_authenticate(user=self.vendor)
        response = self.client.put(self.read_update_delete_url, self.update_data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Stadium.objects.filter(
            vendor=self.vendor, name='stadium3', address='address3', contact='contact3', price_per_hour=300.00,
        ).count(), 1)
        self.assertEqual(Stadium.objects.get(id=response.json()['id']).lat, 30.123)
        self.assertEqual(Stadium.objects.get(id=response.json()['id']).lon, 30.123)

    def test_delete(self):
        self.client.force_authenticate(user=self.vendor)
        response = self.client.delete(self.read_update_delete_url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Stadium.objects.filter().count(), 1)

    def test_book_stadium(self):
        url = f'/api/v1/stadium/stadium_booking/'
        data = {
            'stadium': self.stadium1.id, 'start_time': '2023-01-01 10:00:00', 'end_time': '2023-01-01 11:00:00'
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(StadiumBooking.objects.filter(
            stadium=self.stadium1, start_time='2023-01-01 10:00:00', end_time='2023-01-01 11:00:00',
            user=self.user
        ).count(), 1)

    def test_list_booked_stadiums(self):
        url = f'/api/v1/stadium/stadium_booking/'
        self.client.force_authenticate(user=self.vendor)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_delete_booking(self):
        url = f'/api/v1/stadium/stadium_booking/{self.stb1.id}/'
        self.client.force_authenticate(user=self.vendor)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(StadiumBooking.objects.count(), 1)

    def test_order_stadium_by_distance(self):
        url = self.create_read_url + '?order_by_distance=True&lat=30.123&lon=30.123'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['lon'], 50.123)

    def test_filter_by_start_end_time_2free(self):
        url = self.create_read_url + '?start_time=2021-01-01 7:30:00&end_time=2021-01-01 8:30:00'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_filter_by_start_end_time_1free(self):
        url = self.create_read_url + '?start_time=2021-01-01 10:30:00&end_time=2021-01-01 11:30:00'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_filter_by_start_end_time_0free(self):
        url = self.create_read_url + '?start_time=2021-01-01 10:30:00&end_time=2021-01-01 22:30:00'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

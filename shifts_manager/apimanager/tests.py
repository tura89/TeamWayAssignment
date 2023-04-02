from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Worker, Shift


# Create your tests here.
class ApiManagerTestCase(APITestCase):

    def setUp(self):
        self.worker = Worker.objects.create(name="Bill Gates")
        self.shift = Shift.objects.create(
            worker_id=1,
            shift_date="2022-01-01",
            shift_start="08:00",
            shift_end="16:00"
        )

    def test_worker_create_success(self):
        data = {
            "name": "John Doe"
        }
        response = self.client.post(reverse('all-workers'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_worker_create_blank_name(self):
        invalid_data = {
            "name": ""
        }
        url = reverse('all-workers')
        response = self.client.post(url, invalid_data, format='json')
        content = response.json()
        contains_error_message = "field may not be blank" in content['name'][0]
        self.assertTrue(contains_error_message)

    def worker_create_short_name(self):
        invalid_data = {
            "name": "J"
        }
        url = reverse('all-workers')
        response = self.client.post(url, invalid_data, format='json')
        content = response.json()
        contains_error_message = "should be at least" in content['name'][0]
        self.assertTrue(contains_error_message)

    def test_get_workers(self):
        response = self.client.get(reverse('all-workers'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        content = response.json()
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0], {'id': 1, 'name': 'Bill Gates'})

    def test_get_specific_worker(self):
        response = self.client.get(reverse('worker', args=(self.worker.id,)), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        content = response.json()
        self.assertEqual(content, {'id': 1, 'name': 'Bill Gates'})

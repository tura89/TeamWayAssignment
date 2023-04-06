from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .models import Shift, Worker


# Create your tests here.
class ApiManagerTestCase(APITestCase):
    def setUp(self):
        self.profile = User.objects.create_user(
            username="test_user", password="test_pass"
        )

        self.token = Token.objects.get(user__username="test_user")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        self.worker = Worker.objects.create(name="Bill Gates")
        self.shift = Shift.objects.create(
            worker_id=1, shift_date="2022-01-01", shift_start="08:00", shift_end="16:00"
        )

    def test_worker_create_success(self):
        data = {"name": "John Doe"}
        response = self.client.post(reverse("all-workers"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        content = response.json()
        self.assertEqual(content, {"id": 2, "name": "John Doe"})

    def test_worker_create_blank_name(self):
        invalid_data = {"name": ""}
        url = reverse("all-workers")
        response = self.client.post(url, invalid_data, format="json")

        content = response.json()
        contains_error_message = "field may not be blank" in content["name"][0]
        self.assertTrue(contains_error_message)

    def test_worker_create_short_name(self):
        invalid_data = {"name": "J"}
        url = reverse("all-workers")
        response = self.client.post(url, invalid_data, format="json")
        content = response.json()
        contains_error_message = "should be at least" in content["name"][0]
        self.assertTrue(contains_error_message)

    def test_worker_update(self):
        initial_data = {"name": "Jane Doe"}
        url = reverse("all-workers")
        response = self.client.post(url, initial_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(content, {"id": 2, "name": "Jane Doe"})

        new_data = {"name": "Jill Doe"}
        url = reverse("worker", args=[content["id"]])
        response = self.client.put(url, new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"id": content["id"], "name": "Jill Doe"})

    def test_get_workers(self):
        response = self.client.get(reverse("all-workers"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        content = response.json()
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0], {"id": 1, "name": "Bill Gates"})

    def test_get_specific_worker(self):
        response = self.client.get(
            reverse("worker", args=(self.worker.id,)), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        content = response.json()
        self.assertEqual(content, {"id": 1, "name": "Bill Gates"})

    def test_get_worker_shifts(self):
        response = self.client.get(
            reverse("all-shifts-by-worker", args=(self.worker.id,)), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        content = response.json()
        self.assertEqual(
            content,
            [
                {
                    "id": 1,
                    "worker_id": 1,
                    "shift_date": "2022-01-01",
                    "shift_start": "08:00",
                    "shift_end": "16:00",
                }
            ],
        )

    def test_get_all_shifts(self):
        response = self.client.get(reverse("all-shifts"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        content = response.json()
        self.assertEqual(
            content,
            [
                {
                    "id": 1,
                    "worker_id": 1,
                    "shift_date": "2022-01-01",
                    "shift_start": "08:00",
                    "shift_end": "16:00",
                }
            ],
        )

    def test_create_shift(self):
        data = {
            "worker_id": 1,
            "shift_date": "2022-05-01",
            "shift_start": "16:00",
            "shift_end": "00:00",
        }
        response = self.client.post(reverse("all-shifts"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        content = response.json()
        self.assertEqual(
            content,
            {
                "id": 2,
                "worker_id": 1,
                "shift_date": "2022-05-01",
                "shift_start": "16:00",
                "shift_end": "00:00",
            },
        )

    def test_cr_shift_bad_worker_id(self):
        data = {
            "worker_id": 5,
            "shift_date": "2022-05-01",
            "shift_start": "16:00",
            "shift_end": "00:00",
        }
        response = self.client.post(reverse("all-shifts"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        content = response.json()
        self.assertEqual(content, {"worker_id": ["Worker ID not found"]})

    def test_cr_shift_occupied_date(self):
        data = {
            "worker_id": 1,
            "shift_date": "2022-01-01",
            "shift_start": "16:00",
            "shift_end": "00:00",
        }
        response = self.client.post(reverse("all-shifts"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        content = response.json()
        self.assertEqual(
            content,
            {"non_field_errors": ["Worker 1 already has a shift on 2022-01-01, ID: 1"]},
        )

    def test_cr_shift_invalid_time(self):
        data = {
            "worker_id": 1,
            "shift_date": "2022-05-01",
            "shift_start": "05:00",
            "shift_end": "08:00",
        }
        response = self.client.post(reverse("all-shifts"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        content = response.json()
        self.assertEqual(
            content,
            {
                "shift_start": [
                    "Start date should be one of: ['00:00', '08:00', '16:00']"
                ]
            },
        )

    def test_cr_shift_time_mismatch(self):
        data = {
            "worker_id": 1,
            "shift_date": "2022-05-01",
            "shift_start": "16:00",
            "shift_end": "16:00",
        }
        response = self.client.post(reverse("all-shifts"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        content = response.json()
        self.assertEqual(
            content,
            {
                "non_field_errors": [
                    "End date should be 8 hours ahead of start date, or left unspecified"
                ]
            },
        )

    def test_get_specific_shift(self):
        response = self.client.get(
            reverse("shift", args=(self.shift.id,)), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        content = response.json()
        self.assertEqual(
            content,
            {
                "id": 1,
                "worker_id": 1,
                "shift_date": "2022-01-01",
                "shift_start": "08:00",
                "shift_end": "16:00",
            },
        )

    def test_update_shift(self):
        data = {
            "worker_id": 1,
            "shift_date": "2022-05-01",
            "shift_start": "08:00",
            "shift_end": "16:00",
        }

        response = self.client.put(
            reverse("shift", args=(self.shift.id,)), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        content = response.json()
        self.assertEqual(
            content,
            {
                "id": 1,
                "worker_id": 1,
                "shift_date": "2022-05-01",
                "shift_start": "08:00",
                "shift_end": "16:00",
            },
        )

    def test_delete_shift(self):
        data = {
            "worker_id": 1,
            "shift_date": "2001-01-01",
            "shift_start": "16:00",
            "shift_end": "00:00",
        }
        response = self.client.post(reverse("all-shifts"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(
            reverse("shift", args=(response.json()["id"],)), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

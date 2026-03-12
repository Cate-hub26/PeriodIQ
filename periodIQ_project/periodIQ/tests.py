from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import PeriodEntry
from unittest.mock import patch
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class CycleSummaryViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='nzisa', password='securepass')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('cycle-summary')  

        # Sample entries
        PeriodEntry.objects.create(
            user=self.user,
            start_date=timezone.now().date() - timedelta(days=30),
            end_date=timezone.now().date() - timedelta(days=26)
        )
        PeriodEntry.objects.create(
            user=self.user,
            start_date=timezone.now().date() - timedelta(days=60),
            end_date=timezone.now().date() - timedelta(days=56)
        )

    def test_summary_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('average_cycle_length', response.data)
        self.assertIn('average_period_duration', response.data)
        self.assertEqual(response.data['entry_count'], 2)
        
    def test_summary_with_no_entries(self):
        self.client.force_authenticate(user=self.user)
        PeriodEntry.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['average_cycle_length'], 0.0)
        self.assertEqual(response.data['average_period_duration'], 0)
        self.assertEqual(response.data['entry_count'], 0)

class ConsistencyCheckTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='nzisa', password='securepass')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('consistency-check')  

    def test_valid_timestamps(self):
        data = {
            "timestamps": ["2025-08-01", "2025-08-29", "2025-09-26"]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("is_consistent", response.data)  

    def test_invalid_format(self):
        data = {
            "timestamps": ["01-08-2025", "2025/08/29"]
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)

    def test_non_list_input(self):
        data = {
            "timestamps": "2025-08-01"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)

class PeriodEntryCRUDTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='nzisa', password='secpass')
        self.client.force_authenticate(user=self.user)
        self.list_url = reverse('periodentry-list-create')
        self.entry = PeriodEntry.objects.create(
            user=self.user,
            start_date=timezone.now().date() - timedelta(days=30),
            end_date=timezone.now().date() - timedelta(days=26)
        )
        self.detail_url = reverse(
            'periodentry-retrieve-update-destroy', args=[self.entry.id]
        )
        
    def test_create_period_entry(self):
        data = {
            "start_date": str(timezone.now().date() - timedelta(days=10)),
            "end_date": str(timezone.now().date() - timedelta(days=7))
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(PeriodEntry.objects.count(), 2)
        
    def test_read_period_entries(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        
    def test_update_period_entry(self):
        data = {
            "start_date": str(timezone.now().date() - timedelta(days=31)),
            "end_date": str(timezone.now().date() - timedelta(days=27))
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.start_date, timezone.now().date() - timedelta(days=31))

    def test_delete_period_entry(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(PeriodEntry.objects.count(), 0)

#class PredictionViewTests(APITestCase):
    #def setUp(self):
        #self.user = User.objects.create_user(username="testuser", password="testpass123")
        #self.client = APIClient()
        #self.client.force_authenticate(user=self.user)
        #self.url = reverse("prediction")  # Make sure your URL name matches

    #@patch("periodIQ.utils.predictions.predict_next_period")
    #def test_valid_cycle_data_returns_prediction(self, mock_predict):
        #mock_predict.return_value = {"next_period": "2025-09-22"}

        #payload = {
            #"cycle_data": [28, 30, 27]
        #}

        #response = self.client.post(self.url, payload, format="json")

        #self.assertEqual(response.status_code, status.HTTP_200_OK)
        #self.assertEqual(response.data, {"next_period": "2025-09-22"})
        #mock_predict.assert_called_once_with([28, 30, 27])

   #@patch("periodIQ.utils.predictions.predict_next_period")
    #def test_invalid_cycle_data_returns_error(self, mock_predict):
        #mock_predict.return_value = {"error": "Insufficient data"}

        #payload = {
            #"cycle_data": []
        #}

        #response = self.client.post(self.url, payload, format="json")

        #self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        #self.assertEqual(response.data, {"error": "Insufficient data"})
        #mock_predict.assert_called_once_with([])

    #def test_unauthenticated_request_is_denied(self):
        #self.client.force_authenticate(user=None)
        #response = self.client.post(self.url, {"cycle_data": [28, 29]}, format="json")
        #self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
        
        

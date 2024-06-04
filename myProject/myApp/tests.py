from django.test import TestCase
from .models import WorkingHour  # Assuming your model is in working_hours.models
from .views import workingHour_upload  # Assuming your function is in working_hours.views

from django.test import TestCase

class WorkingHourUploadTest(TestCase):
    def test_successful_upload(self):
        # Create valid data for the form
        data = {
            'day_of_week': 1,  # Monday
            'start_time': '10:00:00',
            'end_time': '12:00:00',
        }

        # Simulate a POST request
        response = self.client.post('/workingHour/upload/', data=data)

        # Assert successful response and expected JSON content
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertJSONContains(response.content, {'message': 'Working hour added to session successfully!', 'status': 'success'})

    def test_invalid_data(self):
        # Create data with missing required field
        data = {
            'start_time': '10:00:00',
            'end_time': '12:00:00',
        }

        # Simulate a POST request
        response = self.client.post('/workingHour/upload/', data=data)

        # Assert form validation error and expected JSON content
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertJSONContains(response.content, {'message': 'Form validation failed', 'status': 'error'})

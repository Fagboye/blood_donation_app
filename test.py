import unittest
from app import app
from models import db, User

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.db = db

    def test_register(self):
        # Test that registration works correctly
        response = self.app.post('/register', json={
            'username': 'testuser',
            'password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
            'gender': 'male',
            'blood_group': 'A+'
        })

        if response.get_json().get("error") == "Username already exists":
            self.assertEqual(response.status_code, 400)
        else:
            self.assertEqual(response.status_code, 200)

    def test_login(self):
        # Test that login works correctly
        response = self.app.post('/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)

    # Add more tests as needed...

    def test_schedule_appointment(self):
        # Test that scheduling an appointment works correctly
        response = self.app.post('/schedule', json={
            'schedule_date': '2022-12-31'
        }, headers={'Authorization': 'Bearer YOUR_TEST_TOKEN'})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
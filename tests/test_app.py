import unittest
import json

import os
import sys

# מוסיפים את תיקיית הפרויקט (התיקייה שמעל tests) ל-PYTHONPATH
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from app import app  



class BMITestCase(unittest.TestCase):
    def setUp(self):
        # before each test – יוצרים test client של Flask
        self.client = app.test_client()

    def test_status_ok(self):
        """בודק ש-/status מחזיר 200 ו-json נכון."""
        response = self.client.get("/status")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIsNotNone(data)
        self.assertEqual(data.get("status"), "ok")

    def test_bmi_normal_weight(self):
        """
        בדיקה ל /bmi עם קלט תקין שבו ה-BMI אמור להיות בטווח 'Normal weight'.
        לדוגמה: weight=70, height=1.75 → בערך 22.86.
        """
        payload = {
            "weight": 70,
            "height": 1.75,
        }
        response = self.client.post(
            "/bmi",
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIsNotNone(data)
        self.assertIn("bmi", data)
        self.assertIn("category", data)

        self.assertAlmostEqual(data["bmi"], 22.86, places=2)
        self.assertEqual(data["category"], "Normal weight")

    def test_bmi_underweight(self):
        """בדיקה לקטגוריה 'Underweight'."""
        payload = {
            "weight": 45,
            "height": 1.7,
        }
        response = self.client.post(
            "/bmi",
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["category"], "Underweight")


    def test_bmi_invalid_numbers(self):
        """בודק טיפול בקלט לא מספרי."""
        payload = {
            "weight": "abc",
            "height": 1.75,
        }
        response = self.client.post(
            "/bmi",
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    def test_bmi_negative_values(self):
        """בודק טיפול בערכים שליליים / אפס."""
        payload = {
            "weight": -10,
            "height": 1.75,
        }
        response = self.client.post(
            "/bmi",
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)


if __name__ == "__main__":
    unittest.main()
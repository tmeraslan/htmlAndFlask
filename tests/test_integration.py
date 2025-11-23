

import os
import requests
import pytest


BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")


@pytest.mark.integration
def test_status_ok_integration():
    url = f"{BASE_URL}/status"
    resp = requests.get(url, timeout=5)
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("status") == "ok"

@pytest.mark.integration
def test_bmi_normal_weight_integration():
    
    url = f"{BASE_URL}/bmi"
    payload = {
        "weight" : 70,
        "height" : 1.75
    }
    resp = requests.post(url, json=payload, timeout=5)
    assert resp.status_code == 200
    data = resp.json()

    assert "bmi" in data
    assert "category" in data

    assert round(data["bmi"]  , 2) == 22.86
    assert data["category"] == "Normal weight"


@pytest.mark.integration
def test_bmi_invalid_input_integration():
    """בודק טיפול בקלט לא תקין: weight לא מספר."""
    url = f"{BASE_URL}/bmi"
    payload = {
        "weight": "abc",
        "height": 1.75,
    }

    resp = requests.post(url, json=payload, timeout=5)

    assert resp.status_code == 400
    data = resp.json()
    assert "error" in data


@pytest.mark.integration
def test_bmi_negative_values_integration():
    """בודק טיפול בערכים שליליים."""
    url = f"{BASE_URL}/bmi"
    payload = {
        "weight": -10,
        "height": 1.75,
    }

    resp = requests.post(url, json=payload, timeout=5)

    assert resp.status_code == 400
    data = resp.json()
    assert "error" in data



# pytest -m integration

# //אם תרצה להריץ unit בלבד (אלה בלי marker integration), אפשר:
# pytest -m "not integration"



# tests/test_ui_selenium.py

import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# ה-URL של האפליקציה – אפשר לשנות ב-CI עם BASE_URL
BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")


@pytest.fixture
def driver():
    """יוצר דפדפן Chrome (headless) לבדיקה וסוגר אותו בסיום."""
    options = webdriver.ChromeOptions()

    # ב-CI צריך headless. מקומית אפשר להוריד את השורה אם רוצים לראות את הדפדפן.
    # options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )
    yield driver
    driver.quit()


@pytest.mark.ui
@pytest.mark.integration
def test_homepage_has_form_and_title(driver):
    """בודק שהעמוד נטען, הכותרת נכונה והטופס קיים."""
    driver.get(f"{BASE_URL}/")

    # כותרת הדף או ה-h1
    h1 = driver.find_element(By.TAG_NAME, "h1").text
    assert "BMI" in h1

    # שדות הקלט
    weight_input = driver.find_element(By.ID, "weight")
    height_input = driver.find_element(By.ID, "height")
    button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    assert weight_input.is_displayed()
    assert height_input.is_displayed()
    assert button.is_displayed()

    time.sleep(1)


# @pytest.mark.ui
# @pytest.mark.integration
# def test_bmi_happy_path_via_ui(driver):
#     """
#     תרחיש תקין:
#     - ממלאים weight=70, height=1.75
#     - לוחצים על Calculate
#     - מחכים לתוצאה
#     - בודקים ערך BMI וקטגוריה
#     """
#     driver.get(f"{BASE_URL}/")

#     weight_input = driver.find_element(By.ID, "weight")
#     height_input = driver.find_element(By.ID, "height")
#     button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

#     weight_input.clear()
#     height_input.clear()
#     weight_input.send_keys("70")
#     height_input.send_keys("1.75")
#     button.click()

#     wait = WebDriverWait(driver, 5)

#     # מחכים שה-div של התוצאה יהיה גלוי
#     result_div = wait.until(
#         EC.visibility_of_element_located((By.ID, "result"))
#     )

#     bmi_value_el = driver.find_element(By.ID, "bmi-value")
#     bmi_category_el = driver.find_element(By.ID, "bmi-category")

#     bmi_text = bmi_value_el.text.strip()
#     category_text = bmi_category_el.text.strip()

#     # בודקים שהטקסט נראה הגיוני
#     assert bmi_text != ""
#     # אפשר גם להמיר ל-float
#     bmi_float = float(bmi_text)
#     assert round(bmi_float, 2) == 22.86

#     assert "Normal" in category_text or "Normal weight" in category_text


# @pytest.mark.ui
# @pytest.mark.integration
# def test_invalid_input_shows_error_message(driver):
#     """
#     תרחיש שגוי:
#     - מכניסים weight לא מספרי
#     - מצפים לראות הודעת שגיאה ב-div עם id="error"
#     """
#     driver.get(f"{BASE_URL}/")

#     weight_input = driver.find_element(By.ID, "weight")
#     height_input = driver.find_element(By.ID, "height")
#     button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

#     weight_input.clear()
#     height_input.clear()
#     weight_input.send_keys("abc")  # לא מספר
#     height_input.send_keys("1.75")
#     button.click()

#     wait = WebDriverWait(driver, 5)

#     error_div = wait.until(
#         EC.visibility_of_element_located((By.ID, "error"))
#     )
#     error_text = error_div.text.strip()

#     assert error_text != ""
#     assert "number" in error_text or "must be" in error_text






# pytest tests/test_ui_selenium.py -m ui

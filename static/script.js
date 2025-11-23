// אם ה-UI מוגש מאותו שרת Flask (Option A), אין צורך ב-API_BASE – פשוט משתמשים בנתיב יחסי.
// אם תרצה להשתמש באפשרות B (שרת נפרד), אפשר להגדיר:
// const API_BASE = "http://localhost:5000";



const form = document.getElementById("bmi-form");
const errorDiv = document.getElementById("error");
const resultDiv = document.getElementById("result");
const bmiValueSpan = document.getElementById("bmi-value");
const bmiCategorySpan = document.getElementById("bmi-category");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  errorDiv.textContent = "";
  resultDiv.style.display = "none";

  const weightInput = document.getElementById("weight");
  const heightInput = document.getElementById("height");

  const weight = parseFloat(weightInput.value);
  const height = parseFloat(heightInput.value);

  // ולידציה בסיסית בצד לקוח
  if (isNaN(weight) || isNaN(height)) {
    errorDiv.textContent = "Please enter valid numbers for weight and height.";
    return;
  }

  if (weight <= 0 || height <= 0) {
    errorDiv.textContent = "Weight and height must be positive.";
    return;
  }

  try {
    const response = await fetch("/bmi", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        weight: weight,
        height: height,
      }),
    });

    if (!response.ok) {
      const errData = await response.json().catch(() => null);
      const msg = errData && errData.error ? errData.error : "Server error";
      errorDiv.textContent = msg;
      return;
    }

    const data = await response.json();

    bmiValueSpan.textContent = data.bmi;
    bmiCategorySpan.textContent = data.category;
    resultDiv.style.display = "block";
  } catch (err) {
    console.error(err);
    errorDiv.textContent = "Failed to connect to the server.";
  }
});

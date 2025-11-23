# BMI Calculator – Flask + HTML/CSS/JS

A simple web application that calculates **Body Mass Index (BMI)**.

- Backend: Flask (Python)
- Frontend: Plain HTML/CSS/JavaScript, served by Flask
- Dockerized: Single image running both API + UI on port **5000**
- CI/CD: GitHub Actions – tests, lint, build & push Docker image

---

## 1. Project Structure

```text
htmlAndFlask/
├── app.py                # Flask application (API + UI)
├── requirements.txt      # Python dependencies
├── Dockerfile            # Container definition
├── pytest.ini            # pytest config (markers)
├── templates/
│   └── index.html        # UI HTML
├── static/
│   ├── styles.css        # UI styling
│   └── script.js         # Frontend logic (fetch /bmi)
└── tests/
    ├── test_app.py       # Unit tests (Flask test_client)
    └── test_integration.py  # Integration tests (requests → http://localhost:5000)
2. Running the App Locally (without Docker)
2.1. Prerequisites
Python 3.9+ installed

pip installed

2.2. Create and activate a virtual environment
bash
Copy code
cd htmlAndFlask

python -m venv venv
# On macOS / Linux:
source venv/bin/activate
# On Windows (PowerShell):
# venv\Scripts\Activate.ps1
2.3. Install dependencies
bash
Copy code
pip install --upgrade pip
pip install -r requirements.txt
2.4. Run the Flask app
bash
Copy code
python app.py
By default Flask will listen on:

text
Copy code
http://127.0.0.1:5000/
3. Accessing the UI and Using the BMI Calculator
Once the server is running (either locally or in Docker):

Open your browser and go to:

text
Copy code
http://localhost:5000/
You’ll see a simple form with:

Weight (kg)

Height (m)

Steps:

Enter weight in kilograms (e.g. 70)

Enter height in meters (e.g. 1.75)

Click "Calculate"

The UI will:

Send a POST /bmi request to the backend

Display:

The calculated BMI (rounded to 2 decimal places)

The category:

< 18.5 → Underweight

18.5–24.9 → Normal weight

25–29.9 → Overweight

>= 30 → Obesity

4. API Endpoints
GET /status
Health check endpoint.

Response:

json
Copy code
{
  "status": "ok"
}
POST /bmi
Request JSON:

json
Copy code
{
  "weight": 70,
  "height": 1.75
}
Response JSON (example):

json
Copy code
{
  "bmi": 22.86,
  "category": "Normal weight"
}
Error examples:

Missing body:

json
Copy code
{ "error": "Missing JSON body" }
Invalid numbers:

json
Copy code
{ "error": "Weight and height must be numbers" }
Non-positive values:

json
Copy code
{ "error": "Weight and height must be positive" }
5. Running Tests Locally
We use pytest for tests, with unit tests and integration tests.

5.1. Install test dependencies
(If not already installed)

bash
Copy code
pip install -r requirements.txt
Make sure pytest and requests are included there.

5.2. Unit tests (no Docker required)
Unit tests use Flask.test_client() and do not require a running server.

bash
Copy code
pytest -m "not integration"
This runs tests like those in tests/test_app.py.

5.3. Integration tests (require running app)
Integration tests send real HTTP requests using requests to a running server.

By default, they use:

text
Copy code
BASE_URL = http://localhost:5000
You can override this with an environment variable:

bash
Copy code
export BASE_URL="http://localhost:5000"
pytest -m integration
Important: For integration tests to pass, the app must be running on BASE_URL
(either via python app.py or Docker, see below).

6. Docker – Build and Run the Image
The Docker image includes both:

Flask backend

Static UI (HTML/CSS/JS) served by Flask

6.1. Build Docker image
From the project root (htmlAndFlask):

bash
Copy code
docker build -t bmi-app .
6.2. Run the container
bash
Copy code
docker run -d -p 5000:5000 --name bmi-app-container bmi-app
This maps container port 5000 to host 5000.

Now you can access:

UI: http://localhost:5000/

Status: http://localhost:5000/status

6.3. Stop and remove the container
bash
Copy code
docker stop bmi-app-container
docker rm bmi-app-container
7. Integration Tests Against the Container
Typically used in CI, but can also run locally.

Build and run the container:

bash
Copy code
docker build -t bmi-app:test .
docker run -d -p 5000:5000 --name bmi-app-test bmi-app:test
(Optional) Wait and check health:

bash
Copy code
curl http://localhost:5000/status
Run integration tests:

bash
Copy code
export BASE_URL="http://localhost:5000"
pytest -m integration
Cleanup:

bash
Copy code
docker stop bmi-app-test
docker rm bmi-app-test
8. CI/CD Pipeline (GitHub Actions)
The repository includes a workflow file (e.g. .github/workflows/ci.yml) that defines a simple CI/CD pipeline with three jobs:

8.1. tests-and-lint job
Triggered on:

push to main

pull_request to main

Steps:

Check out the code.

Set up Python.

Install dependencies (pip install -r requirements.txt, flake8).

Run linter:

bash
Copy code
flake8 app.py tests
Run unit tests (exclude integration):

bash
Copy code
pytest -m "not integration"
If this job fails, the pipeline stops (no Docker build/push).

8.2. integration-tests job
Runs after tests-and-lint (needs: tests-and-lint).

Steps:

Check out code.

Set up Python and install dependencies (including requests).

Build Docker image for tests:

bash
Copy code
docker build -t bmi-app:test .
Run container:

bash
Copy code
docker run -d -p 5000:5000 --name bmi-app-test bmi-app:test
Wait until /status is healthy (using curl with retries).

Run integration tests:

bash
Copy code
pytest -m integration
Always stop & remove the container at the end (even on failure).

If this job fails, the Docker image will not be pushed.

8.3. build-and-push job
Runs only on push to main (not on PRs).

Depends on both previous jobs:

yaml
Copy code
needs: [tests-and-lint, integration-tests]
Requires the following GitHub Secrets:

DOCKERHUB_USERNAME – your Docker Hub username

DOCKERHUB_TOKEN – Docker Hub access token (from Docker Hub UI)

Steps:

Login to Docker Hub:

bash
Copy code
echo "${DOCKERHUB_TOKEN}" | docker login -u "${DOCKERHUB_USERNAME}" --password-stdin
Build image with two tags:

bash
Copy code
IMAGE_NAME=${DOCKERHUB_USERNAME}/bmi-app

docker build -t $IMAGE_NAME:${GITHUB_SHA} -t $IMAGE_NAME:latest .
Push both tags:

bash
Copy code
docker push $IMAGE_NAME:${GITHUB_SHA}
docker push $IMAGE_NAME:latest
Result:

Every successful push to main:

Runs lint + tests (unit + integration)

Builds and pushes a new Docker image to Docker Hub

You always have:

A unique image tag per commit: bmi-app:<commit-sha>

The latest image: bmi-app:latest

9. Summary
Locally (dev):

python app.py → run app on localhost:5000

pytest -m "not integration" → unit tests

pytest -m integration → integration tests (requires running app)

Docker:

docker build -t bmi-app .

docker run -d -p 5000:5000 bmi-app

Open http://localhost:5000/ to use the BMI UI

CI/CD (GitHub Actions):

On PRs: lint + unit tests + integration tests

On push to main: all tests + build & push Docker image to Docker Hub

go
Copy code

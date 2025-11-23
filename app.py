from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "ok"})


def calculate_bmi_category(bmi: float) -> str:

    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obesity"
    

@app.route("/bmi", methods=["POST"])
def bmi():

    data = request.get_json()
    if not data:
        return jsonify({"error":"Missing JSON body"}), 400
    
    weight = data.get("weight")
    height = data.get("height")

    try:
        weight = float(weight)
        height = float(height)
    except (TypeError, ValueError):
        return jsonify({"error":"Weight and height must be numbers"}),400
    
    if weight <= 0 or height <= 0:
        return jsonify({"error":"Weight and height must be positive"}), 400
    
    bmi_value = weight / (height * height)
    bmi_rounded = round(bmi_value, 2)

    category = calculate_bmi_category(bmi_rounded)

    return jsonify({
        "bmi":bmi_rounded,
        "category":category
    })
    



@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0", port=5000, debug=True)




# python3 -m venv venv
# source venv/bin/activate
# venv\Scripts\activate


# pip install flask
# pip install -r requirements.txt


# python app.py


#/בדיקות שחייבים לעשות
# http://localhost:5000/status



# curl -X POST http://localhost:5000/bmi \
#   -H "Content-Type: application/json" \
#   -d '{"weight": 70, "height": 1.75}'


from flask import Flask, request, jsonify

app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return "Shipping App is running 🚀"

# Shipping cost calculator
@app.route("/shipping", methods=["GET"])
def shipping():
    try:
        weight = float(request.args.get("weight", 1))
        distance = float(request.args.get("distance", 1))

        cost = (weight * 5) + (distance * 0.5)

        return jsonify({
            "weight": weight,
            "distance": distance,
            "shipping_cost": cost
        })

    except:
        return jsonify({"error": "Invalid input"})

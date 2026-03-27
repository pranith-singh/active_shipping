from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# UI Page
@app.route("/")
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Shipping App</title>
    </head>
    <body style="font-family: Arial; text-align:center; margin-top:50px;">
        <h1>🚚 Shipping Calculator</h1>

        <input id="weight" type="number" placeholder="Enter weight" /><br><br>
        <input id="distance" type="number" placeholder="Enter distance" /><br><br>

        <button onclick="calculate()">Calculate</button>

        <h2 id="result"></h2>

        <script>
            function calculate() {
                let weight = document.getElementById("weight").value;
                let distance = document.getElementById("distance").value;

                fetch(`/shipping?weight=${weight}&distance=${distance}`)
                .then(res => res.json())
                .then(data => {
                    document.getElementById("result").innerText =
                        "Shipping Cost: " + data.shipping_cost;
                });
            }
        </script>
    </body>
    </html>
    """)

# API
@app.route("/shipping")
def shipping():
    try:
        weight = float(request.args.get("weight", 1))
        distance = float(request.args.get("distance", 1))

        cost = (weight * 5) + (distance * 0.5)

        return jsonify({"shipping_cost": cost})
    except:
        return jsonify({"error": "Invalid input"})

from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

@app.route("/")
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Shipping App</title>
        <style>
            body {
                font-family: Arial;
                background: #f4f6f8;
                text-align: center;
                padding: 50px;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                width: 300px;
                margin: auto;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            input, select {
                width: 90%;
                padding: 10px;
                margin: 10px;
                border-radius: 5px;
                border: 1px solid #ccc;
            }
            button {
                padding: 10px 20px;
                background: #0078D4;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background: #005fa3;
            }
            h1 {
                margin-bottom: 20px;
            }
            #result {
                margin-top: 20px;
                font-size: 18px;
                font-weight: bold;
            }
        </style>
    </head>
    <body>

        <div class="container">
            <h1>🚚 Shipping App</h1>

            <input id="weight" type="number" placeholder="Weight (kg)" />
            <input id="distance" type="number" placeholder="Distance (km)" />

            <select id="type">
                <option value="standard">Standard</option>
                <option value="express">Express</option>
            </select>

            <button onclick="calculate()">Calculate</button>

            <div id="result"></div>
        </div>

        <script>
            function calculate() {
                let weight = document.getElementById("weight").value;
                let distance = document.getElementById("distance").value;
                let type = document.getElementById("type").value;

                fetch(`/shipping?weight=${weight}&distance=${distance}&type=${type}`)
                .then(res => res.json())
                .then(data => {
                    if (data.error) {
                        document.getElementById("result").innerText = data.error;
                    } else {
                        document.getElementById("result").innerText =
                            "Cost: ₹" + data.shipping_cost + " (" + data.type + ")";
                    }
                });
            }
        </script>

    </body>
    </html>
    """)

@app.route("/shipping")
def shipping():
    try:
        weight = float(request.args.get("weight", 1))
        distance = float(request.args.get("distance", 1))
        ship_type = request.args.get("type", "standard")

        # Pricing logic
        cost = (weight * 5) + (distance * 0.5)

        if ship_type == "express":
            cost *= 1.5  # extra charge

        return jsonify({
            "shipping_cost": round(cost, 2),
            "type": ship_type
        })

    except:
        return jsonify({"error": "Invalid input"})

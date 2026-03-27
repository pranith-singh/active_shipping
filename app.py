from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

orders = []  # temporary storage

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
                background: linear-gradient(135deg, #667eea, #764ba2);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                color: white;
            }
            .card {
                background: white;
                color: black;
                padding: 30px;
                border-radius: 15px;
                width: 350px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                text-align: center;
            }
            input, select {
                width: 90%;
                padding: 10px;
                margin: 10px;
                border-radius: 8px;
                border: 1px solid #ccc;
            }
            button {
                padding: 12px 20px;
                background: #667eea;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                width: 95%;
            }
            button:hover {
                background: #5a67d8;
            }
            #result {
                margin-top: 15px;
                font-weight: bold;
            }
        </style>
    </head>
    <body>

        <div class="card">
            <h2>🚚 Shipping App</h2>

            <input id="weight" type="number" placeholder="Weight (kg)">
            <input id="distance" type="number" placeholder="Distance (km)">

            <select id="type">
                <option value="standard">Standard</option>
                <option value="express">Express</option>
            </select>

            <button onclick="calculate()">Calculate & Save</button>

            <div id="result"></div>

            <br>
            <button onclick="viewOrders()">View Orders</button>
        </div>

        <script>
            function calculate() {
                let weight = document.getElementById("weight").value;
                let distance = document.getElementById("distance").value;
                let type = document.getElementById("type").value;

                fetch(`/shipping?weight=${weight}&distance=${distance}&type=${type}`)
                .then(res => res.json())
                .then(data => {
                    document.getElementById("result").innerText =
                        "Cost: ₹" + data.shipping_cost;
                });
            }

            function viewOrders() {
                fetch('/orders')
                .then(res => res.json())
                .then(data => {
                    let text = "Orders:\\n";
                    data.forEach(o => {
                        text += `₹${o.cost} (${o.type})\\n`;
                    });
                    alert(text);
                });
            }
        </script>

    </body>
    </html>
    """)

@app.route("/shipping")
def shipping():
    weight = float(request.args.get("weight", 1))
    distance = float(request.args.get("distance", 1))
    ship_type = request.args.get("type", "standard")

    cost = (weight * 5) + (distance * 0.5)

    if ship_type == "express":
        cost *= 1.5

    order = {"cost": round(cost, 2), "type": ship_type}
    orders.append(order)

    return jsonify({"shipping_cost": order["cost"]})

@app.route("/orders")
def get_orders():
    return jsonify(orders)

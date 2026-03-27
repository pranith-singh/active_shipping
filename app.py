from flask import Flask, request, jsonify, render_template_string
import sqlite3

app = Flask(__name__)

# Create DB + table
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            weight REAL,
            distance REAL,
            type TEXT,
            cost REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Shipping App</title>
    </head>
    <body style="font-family:Arial; text-align:center; margin-top:50px;">

        <h2>🚚 Shipping App</h2>

        <input id="weight" type="number" placeholder="Weight"><br><br>
        <input id="distance" type="number" placeholder="Distance"><br><br>

        <select id="type">
            <option value="standard">Standard</option>
            <option value="express">Express</option>
        </select><br><br>

        <button onclick="calculate()">Calculate & Save</button>
        <button onclick="viewOrders()">View Orders</button>

        <h3 id="result"></h3>

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

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO orders (weight, distance, type, cost) VALUES (?, ?, ?, ?)",
              (weight, distance, ship_type, round(cost, 2)))
    conn.commit()
    conn.close()

    return jsonify({"shipping_cost": round(cost, 2)})

@app.route("/orders")
def get_orders():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT weight, distance, type, cost FROM orders")
    rows = c.fetchall()
    conn.close()

    orders = []
    for r in rows:
        orders.append({
            "weight": r[0],
            "distance": r[1],
            "type": r[2],
            "cost": r[3]
        })

    return jsonify(orders)

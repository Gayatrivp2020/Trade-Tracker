from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Sample data
trades = [
    {"id": 101, "stock": "TCS", "qty": 10, "price": 3500, "days": 1},
    {"id": 102, "stock": "INFY", "qty": 5, "price": 1500, "days": 2},
    {"id": 103, "stock": "HDFC", "qty": 8, "price": 2500, "days": 3},
    {"id": 104, "stock": "RELIANCE", "qty": 3, "price": 2800, "days": 4}
]

def get_status(days):
    if days > 2:
        return "Delayed"
    elif days == 2:
        return "Settled"
    else:
        return "Processing"

@app.route('/trades')
def get_trades():
    result = []
    for t in trades:
        result.append({
            "id": t["id"],
            "stock": t["stock"],
            "qty": t["qty"],
            "price": t["price"],
            "status": get_status(t["days"])
        })
    return jsonify(result)

@app.route('/')
def dashboard():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
<title>Trade Dashboard</title>

<style>
body {
    font-family: Arial;
    background: #f4f6f9;
    margin: 0;
}

.header {
    background: #007bff;
    color: white;
    padding: 15px;
    text-align: center;
    font-size: 22px;
}

.stats {
    display: flex;
    justify-content: space-around;
    margin: 20px;
}

.stat-box {
    background: white;
    padding: 20px;
    border-radius: 10px;
    width: 25%;
    text-align: center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
}

.card {
    background: white;
    margin: 10px;
    padding: 15px;
    border-radius: 10px;
    width: 220px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.processing { color: orange; }
.settled { color: green; }
.delayed { color: red; }

button {
    display: block;
    margin: 20px auto;
    padding: 10px 20px;
    border: none;
    background: #007bff;
    color: white;
    border-radius: 5px;
    cursor: pointer;
}
</style>
</head>

<body>

<div class="header">📊 Trade Settlement Dashboard</div>

<div class="stats">
    <div class="stat-box">
        <h3>Total Trades</h3>
        <p id="total">0</p>
    </div>
    <div class="stat-box">
        <h3>Settled</h3>
        <p id="settled">0</p>
    </div>
    <div class="stat-box">
        <h3>Delayed</h3>
        <p id="delayed">0</p>
    </div>
</div>

<button onclick="loadTrades()">Load Trades</button>

<div class="container" id="data"></div>

<script>
function loadTrades() {
    fetch('/trades')
    .then(res => res.json())
    .then(data => {
        let container = document.getElementById("data");
        container.innerHTML = "";

        let total = data.length;
        let settled = 0;
        let delayed = 0;

        data.forEach(t => {
            let cls = "";

            if (t.status === "Settled") {
                cls = "settled";
                settled++;
            }
            else if (t.status === "Delayed") {
                cls = "delayed";
                delayed++;
            }
            else {
                cls = "processing";
            }

            container.innerHTML += `
                <div class="card">
                    <h3>${t.stock}</h3>
                    <p>ID: ${t.id}</p>
                    <p>Qty: ${t.qty}</p>
                    <p>Price: ₹${t.price}</p>
                    <p class="${cls}">
                        ${t.status}
                    </p>
                </div>
            `;
        });

        document.getElementById("total").innerText = total;
        document.getElementById("settled").innerText = settled;
        document.getElementById("delayed").innerText = delayed;
    });
}
</script>

</body>
</html>
""")

if __name__ == '__main__':
    app.run(debug=True)
from datetime import datetime
from flask import Flask, render_template, request
import random
import uuid

app = Flask(__name__)
last_scan = {}
scan_history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html",
        history=scan_history
    )

@app.route("/scan")
def scan():
    return render_template("scan.html")

@app.route("/loading")
def loading():
    ip = request.args.get("ip")
    return render_template("loading.html", ip=ip)

@app.route("/report")
def report():
    return render_template(
        "report.html",
        ip=last_scan.get("ip", "No Scan"),
        ports=last_scan.get("ports", []),
        risk=last_scan.get("risk", "Unknown"),
        color=last_scan.get("color", "white"),
        date=last_scan.get("date", "Not Available"),
        report_id=last_scan.get("report_id", "Not Generated")
    )

@app.route("/result")
def result():

    global last_scan

    ip = request.args.get("ip")
    ports = [22, 80, 443]

    risk = random.choice(["Low", "Medium", "High"])
    scan_date = datetime.now().strftime("%d %B %Y | %I:%M %p")
    report_id = "CS-" + datetime.now().strftime("%Y%m%d") + "-" + str(uuid.uuid4())[:4].upper()

    if risk == "Low":
        color = "green"
    elif risk == "Medium":
        color = "orange"
    else:
        color = "red"

    last_scan = {
        "ip": ip,
        "ports": ports,
        "risk": risk,
        "color": color,
        "date": scan_date,
        "report_id": report_id
    }
    status = "Secure"

    if risk == "Medium":
        status = "Monitor"
    elif risk == "High":
        status = "Action Required"

    scan_history.insert(0, {
        "ip": ip,
        "risk": risk,
        "status": status
    })

    scan_history[:] = scan_history[:3]

    return render_template(
        "result.html",
        ip=ip,
        ports=ports,
        risk=risk,
        color=color
    )

if __name__ == "__main__":
    app.run(debug=True)
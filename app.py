from flask import Flask, render_template, request
from crew_runner import run_travel_planner

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    reports = None
    if request.method == "POST":
        country = request.form.get("country")
        year = request.form.get("year")
        if country and year:
            reports = run_travel_planner(country, year)
    return render_template("index.html", reports=reports)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8501,
        debug=True,
        use_reloader=False,
    )
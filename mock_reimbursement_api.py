from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

def load_data():
    data = {}
    for file in os.listdir("data"):
        if file.endswith(".csv"):
            key = file.split(".")[0]
            data[key] = pd.read_csv(os.path.join("data", file))
    return data

data_sources = load_data()

@app.route("/check_reimbursement", methods=["POST"])
def check_reimbursement():
    req = request.get_json()
    country = req.get("country", "").lower()
    service = req.get("service", "").lower()

    if country not in data_sources:
        return jsonify({"is_covered": False, "notes": f"No data for country '{country}'."})

    df = data_sources[country]
    match = df[df["service"].str.lower().str.contains(service)]

    if not match.empty:
        row = match.iloc[0]
        return jsonify({
            "is_covered": True,
            "scheme": row["scheme"],
            "item_code": row["item_code"],
            "price": row["price"],
            "notes": row["notes"]
        })

    return jsonify({"is_covered": False, "notes": "Service not found."})

if __name__ == "__main__":
    app.run(debug=True)

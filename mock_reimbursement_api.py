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

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "Reimbursement API is running",
        "available_countries": list(data_sources.keys())
    })

@app.route("/check_reimbursement", methods=["GET", "POST"])
def check_reimbursement():
    try:
        # Handle both GET and POST requests
        if request.method == "GET":
            country = request.args.get("country", "").lower()
            service = request.args.get("service", "").lower()
            code = request.args.get("code", "").lower()
        else:  # POST
            req = request.get_json() or {}
            country = req.get("country", "").lower()
            service = req.get("service", "").lower()
            code = req.get("code", "").lower()

        if not country:
            return jsonify({"is_covered": False, "notes": "Country parameter is required."})

        if country not in data_sources:
            return jsonify({"is_covered": False, "notes": f"No data for country '{country}'."})

        df = data_sources[country]
        
        # Search by service name or item code
        if code:
            # Search by item code
            match = df[df["item_code"].str.lower() == code]
        elif service:
            # Search by service name
            match = df[df["service"].str.lower().str.contains(service)]
        else:
            return jsonify({"is_covered": False, "notes": "Please provide either 'service' or 'code' parameter."})

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
    
    except Exception as e:
        return jsonify({"is_covered": False, "notes": f"Error processing request: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)

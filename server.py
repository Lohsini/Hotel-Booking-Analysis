from flask import Flask, request, jsonify
import pandas as pd
import json

app = Flask(__name__)
csv_path = "hotel_booking_simple.csv"
simple_data = pd.read_csv(csv_path)


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    print(username, password)
    if username in simple_data["phone-number"].values and password in simple_data["token"].values:
        # indices = data.index[data['token'] == password].tolist()
        user_info = simple_data.loc[simple_data['token'] == password]
        return jsonify({"message": "Login successful", "status": "success", "data": json.loads(user_info.to_json(orient='records'))}), 200
    else:
        return jsonify({"message": "Invalid credentials", "status": "fail"}), 401


if __name__ == "__main__":
    app.run(debug=True)

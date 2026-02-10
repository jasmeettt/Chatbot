from flask import Flask, jsonify, request

app = Flask(__name__)

# ✅ Default route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the QuickRail API!"})

# ✅ Expanded station data with local stops from Maharashtra
stations = {
    "NDLS": {"name": "New Delhi", "code": "NDLS"},
    "MMCT": {"name": "Mumbai Central", "code": "MMCT"},
    "HWH": {"name": "Howrah Junction", "code": "HWH"},
    "CSMT": {"name": "Chhatrapati Shivaji Maharaj Terminus", "code": "CSMT"},
    "SBC": {"name": "Bangalore City Junction", "code": "SBC"},
    "MAS": {"name": "Chennai Central", "code": "MAS"},
    "BBS": {"name": "Bhubaneswar", "code": "BBS"},
    "PUNE": {"name": "Pune Junction", "code": "PUNE"},
    "JAT": {"name": "Jammu Tawi", "code": "JAT"},
    "ADI": {"name": "Ahmedabad Junction", "code": "ADI"},
    "TNA": {"name": "Thane", "code": "TNA"},
    "KYN": {"name": "Kalyan Junction", "code": "KYN"},
    "BSR": {"name": "Vasai Road", "code": "BSR"},
    "PNVL": {"name": "Panvel", "code": "PNVL"},
    "DDR": {"name": "Dadar", "code": "DDR"},
    "BVI": {"name": "Borivali", "code": "BVI"},
    "VR": {"name": "Virar", "code": "VR"},
    "BUD": {"name": "Badlapur", "code": "BUD"},
    "KJT": {"name": "Karjat", "code": "KJT"},
    "LNL": {"name": "Lonavala", "code": "LNL"},
    "CCH": {"name": "Chinchvad", "code": "CCH"}
}

# ✅ Expanded train status data
trains = {
    "12431": {"name": "Rajdhani Express", "status": "On Time"},
    "11027": {"name": "Mumbai Mail", "status": "Delayed by 10 min"},
    "12625": {"name": "Kerala Express", "status": "On Time"},
    "12295": {"name": "Sanghamitra Express", "status": "Delayed by 15 min"},
    "12951": {"name": "Mumbai Rajdhani", "status": "On Time"},
    "12301": {"name": "Howrah Rajdhani", "status": "On Time"},
    "12622": {"name": "Tamil Nadu Express", "status": "Delayed by 20 min"},
    "12701": {"name": "Andhra Pradesh Express", "status": "On Time"},
    "12839": {"name": "Chennai Howrah Mail", "status": "Delayed by 30 min"},
    "22120": {"name": "Tejas Express", "status": "On Time"}
}

# ✅ Expanded PNR status data
pnr_data = {
    "1234567890": {"status": "Confirmed", "seat": "B2-23"},
    "9876543210": {"status": "RAC", "seat": "S3-10"},
    "5678901234": {"status": "Waiting List", "seat": "WL-15"},
    "1122334455": {"status": "Confirmed", "seat": "A1-03"}
}

# ✅ Expanded train fare data
train_fares = {
    "12431": {"SL": 500, "3A": 1200, "2A": 1800, "1A": 2500},
    "11027": {"SL": 450, "3A": 1100, "2A": 1700, "1A": 2400},
    "12625": {"SL": 550, "3A": 1300, "2A": 1900, "1A": 2600},
    "12295": {"SL": 600, "3A": 1400, "2A": 2000, "1A": 2700},
    "12951": {"SL": 650, "3A": 1500, "2A": 2100, "1A": 2800},
    "12301": {"SL": 700, "3A": 1600, "2A": 2200, "1A": 2900},
    "12701": {"SL": 620, "3A": 1450, "2A": 2050, "1A": 2750},
    "12839": {"SL": 580, "3A": 1350, "2A": 1950, "1A": 2650},
    "22120": {"SL": 800, "3A": 1700, "2A": 2300, "1A": 3100}
}

# ✅ Station Details Endpoint
@app.route('/station/<station_code>', methods=['GET'])
def get_station_details(station_code):
    station = stations.get(station_code.upper())
    if station:
        return jsonify({"station_details": station})
    return jsonify({"error": f"Station '{station_code}' not found"}), 404

# ✅ Train Live Status Endpoint
@app.route('/train_status/<train_number>', methods=['GET'])
def get_train_status(train_number):
    return jsonify({"train_status": trains.get(train_number, "❌ No train status found!")})

# ✅ PNR Status Endpoint
@app.route('/pnr_status/<pnr_number>', methods=['GET'])
def get_pnr_status(pnr_number):
    return jsonify({"pnr_status": pnr_data.get(pnr_number, "❌ No PNR details found!")})

# ✅ Train Fare Endpoint
@app.route('/train_fare', methods=['GET'])
def get_train_fare():
    train_number = request.args.get("train_number")
    class_type = request.args.get("class")

    if train_number in train_fares and class_type in train_fares[train_number]:
        return jsonify({"train_fare": train_fares[train_number][class_type]})
    return jsonify({"train_fare": "❌ No fare details found!"})

# ✅ Run Flask API
if __name__ == "__main__":
    print("🚀 Running Flask API on http://127.0.0.1:5001")
    app.run(port=5001, debug=True)
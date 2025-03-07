import streamlit as st
import http.client
import json

# RapidAPI Headers (Replace with your actual API key)
HEADERS = {
    "x-rapidapi-key": "4d0dc103a0mshe97cfb09b21c167p12b446jsn8b5b922e8340",
    "x-rapidapi-host": "irctc1.p.rapidapi.com"
}

# Function to get station details
def get_station_details(station_code):
    url = "https://irctc1.p.rapidapi.com/api/v1/searchStation"
    response = requests.get(url, headers=HEADERS, params={"query": station_code})

    if response.status_code == 200:
        try:
            data = response.json()
            if data.get("data"):
                station = data["data"][0]
                return f"🚉 **Station Name**: {station['station_name']} \n🆔 **Code**: {station['station_code']}"
            else:
                return "❌ No station found!"
        except Exception as e:
            return f"⚠️ Error processing station data: {e}"
    return f"❌ API Error! Status Code: {response.status_code}"

# Function to get train live status (using the new API)
def get_train_status(train_number):
    conn = http.client.HTTPSConnection("indian-railway-irctc.p.rapidapi.com")
    
    # Set the API headers
    headers = {
        'x-rapidapi-key': "4d0dc103a0mshe97cfb09b21c167p12b446jsn8b5b922e8340",
        'x-rapidapi-host': "indian-railway-irctc.p.rapidapi.com",
        'x-rapid-api': "rapid-api-database"
    }
    
    # Make the GET request to fetch live train status
    conn.request("GET", f"/api/trains/v1/train/status?train_number={train_number}&departure_date=20240623&isH5=true&client=web", headers=headers)
    
    res = conn.getresponse()
    data = res.read()
    
    # Parse the response
    response_data = json.loads(data.decode("utf-8"))
    
    # Check if the response is valid and contains train data
    if response_data.get("status") == "success":
        train_info = response_data.get("body", {}).get("trains", [])
        
        if not train_info:
            return "❌ No train information found!"

        train_details = train_info[0]  # Assuming the first train in the list is the one we need
        
        # Train details
        train_name = train_details.get("trainName", "Unknown Train")
        origin = train_details.get("origin", "Unknown Origin")
        destination = train_details.get("destination", "Unknown Destination")
        route_details = []
        
        for station in train_details.get("station", []):
            station_name = station.get("stationName", "Unknown Station")
            arrival_time = station.get("arrivalTime", "--")
            departure_time = station.get("departureTime", "--")
            route_details.append(f"📍 **Station**: {station_name} | Arrival: {arrival_time} | Departure: {departure_time}")
        
        route_info = "\n".join(route_details)
        
        return f"🚆 **Train**: {train_name} ({train_number})\n🌍 **From**: {origin} to {destination}\n\n{route_info}"
    
    else:
        return "❌ Failed to fetch live train status."

# Function to check PNR status
def get_pnr_status(pnr_number):
    url = "https://irctc1.p.rapidapi.com/api/v1/checkPNR"
    response = requests.get(url, headers=HEADERS, params={"pnrNumber": pnr_number})

    if response.status_code == 200:
        try:
            data = response.json()
            if "data" in data and data["data"]:
                pnr_info = data["data"]
                return f"🆔 **PNR**: {pnr_number} \n🚆 **Train**: {pnr_info['train_name']} \n📍 **Status**: {pnr_info['passengerStatus']}"
            else:
                return "❌ No PNR details found!"
        except Exception as e:
            return f"⚠️ Error processing PNR data: {e}"
    return "❌ API Error! Unable to fetch PNR status."

# Function to get train fare details
def get_train_fare(train_number, from_station, to_station, class_type, quota):
    url = "https://irctc1.p.rapidapi.com/api/v1/getFare"
    params = {
        "trainNo": train_number,
        "fromStationCode": from_station,
        "toStationCode": to_station,
        "classType": class_type,
        "quota": quota
    }
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code == 200:
        try:
            data = response.json()
            if "data" in data and data["data"]:
                fare_info = data["data"]
                return f"🚆 **Train**: {fare_info['train_name']} \n💰 **Fare**: ₹{fare_info['fare']}"
            else:
                return "❌ No fare details found!"
        except Exception as e:
            return f"⚠️ Error processing fare data: {e}"
    return "❌ API Error! Unable to fetch fare details."

# Streamlit UI
def app():
    st.sidebar.title("🚆 Indian Railways Info")
    option = st.sidebar.radio("🔍 Select an option:", ["🏢 Station Details", "🚆 Train Live Status", "🆔 PNR Status", "💰 Train Fare"])

    st.title("🚆 Indian Railways Information System")
    st.markdown("### Get Real-Time Train & Station Info in a Click!")

    # 🚉 Station Details
    if option == "🏢 Station Details":
        st.subheader("🔎 Search for Station Details")
        station_code = st.text_input("Enter Station Code:")
        if st.button("Get Station Details"):
            with st.spinner("Fetching details..."):
                result = get_station_details(station_code)
                st.success(result)

    # 🚆 Train Live Status
    elif option == "🚆 Train Live Status":
        st.subheader("📍 Check Live Train Status")
        train_number = st.text_input("Enter Train Number:")
        if st.button("Get Train Status"):
            with st.spinner("Fetching details..."):
                result = get_train_status(train_number)
                st.success(result)

    # 🆔 PNR Status
    elif option == "🆔 PNR Status":
        st.subheader("🔍 Check PNR Status")
        pnr_number = st.text_input("Enter PNR Number:")
        if st.button("Get PNR Status"):
            with st.spinner("Fetching details..."):
                result = get_pnr_status(pnr_number)
                st.success(result)

    # 💰 Train Fare
    elif option == "💰 Train Fare":
        st.subheader("💰 Check Train Fare")
        train_number = st.text_input("Enter Train Number:")
        from_station = st.text_input("Enter From Station Code:")
        to_station = st.text_input("Enter To Station Code:")
        class_type = st.selectbox("Select Class Type:", ["SL", "3A", "2A", "1A"])
        quota = st.selectbox("Select Quota:", ["GN", "TQ", "PT", "LD", "SS"])

        if st.button("Get Train Fare"):
            with st.spinner("Fetching details..."):
                result = get_train_fare(train_number, from_station, to_station, class_type, quota)
                st.success(result)

if __name__ == "__main__":
    app()

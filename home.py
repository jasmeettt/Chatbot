import streamlit as st
import requests

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

# Function to get train live status
def get_train_status(train_number):
    url = "https://irctc1.p.rapidapi.com/api/v1/liveTrainStatus"
    response = requests.get(url, headers=HEADERS, params={"trainNo": train_number})

    if response.status_code == 200:
        try:
            data = response.json()
            if "data" in data and data["data"]:
                status = data["data"]
                return f"🚆 **Train**: {status['train_name']} ({train_number})\n📍 **Current Status**: {status['position']}"
        except Exception as e:
            return f"⚠️ Error processing train data: {e}"
    return "❌ No train status found or API error!"

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

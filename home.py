import streamlit as st
import requests

# Set page title and icon
# st.set_page_config(page_title="Indian Railways Info", page_icon="🚆", layout="wide")

# RapidAPI Headers (Replace with your actual API key)
HEADERS = {
    "x-rapidapi-key": "4d0dc103a0mshe97cfb09b21c167p12b446jsn8b5b922e8340",  # Replace with your RapidAPI Key
    "x-rapidapi-host": "irctc1.p.rapidapi.com"
}

# Custom CSS for better UI
st.markdown("""
    <style>
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #002147;
        }

        /* Titles and Headers */
        h1, h2, h3 {
            color: #0033A0;
            font-weight: bold;
        }

        /* Buttons */
        div.stButton > button {
            background-color: #0033A0;
            color: white;
            border-radius: 10px;
            border: none;
            padding: 10px 20px;
        }

        div.stButton > button:hover {
            background-color: #0055CC;
            color: white;
        }

        /* Input fields */
        div[data-baseweb="input"] > div {
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

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

# Function to get PNR status
def get_pnr_status(pnr_number):
    url = "https://irctc1.p.rapidapi.com/api/v1/checkPnrStatus"
    response = requests.get(url, headers=HEADERS, params={"pnrNumber": pnr_number})

    if response.status_code == 200:
        try:
            data = response.json()
            if "data" in data and data["data"]:
                pnr_info = data["data"]
                return f"""
                🆔 **PNR**: {pnr_number}  
                🚆 **Train**: {pnr_info['train_name']} ({pnr_info['train_number']})  
                📅 **Journey Date**: {pnr_info['doj']}  
                🎟️ **Status**: {pnr_info['passenger_status']}
                """
        except Exception as e:
            return f"⚠️ Error processing PNR data: {e}"
    return "❌ No PNR details found or API error!"

# Function to get train fare details
def get_train_fare(train_number, source, destination):
    url = "https://irctc1.p.rapidapi.com/api/v1/getFare"
    response = requests.get(url, headers=HEADERS, params={"trainNo": train_number, "fromStation": source, "toStation": destination})

    if response.status_code == 200:
        try:
            data = response.json()
            if "data" in data and data["data"]:
                fare_info = data["data"]
                return f"🚆 **Train**: {fare_info['train_name']} ({train_number})\n💰 **Fare**: {fare_info['fare']} INR"
        except Exception as e:
            return f"⚠️ Error processing fare data: {e}"
    return "❌ No fare details found or API error!"

# Streamlit UI
def app():
    st.sidebar.title("🚆 Indian Railways Info")

    option = st.sidebar.radio("🔍 Select an option:", ["🏢 Station Details", "🚆 Train Live Status", "🆔 PNR Status", "💰 Train Fare"])

    st.title("🚆 Indian Railways Information System")
    st.markdown("### Get Real-Time Train & Station Info in a Click!")

    if option == "🏢 Station Details":
        st.subheader("🔎 Search for Station Details")
        station_code = st.text_input("Enter Station Code:")
        if st.button("Get Station Details"):
            with st.spinner("Fetching details..."):
                result = get_station_details(station_code)
                st.success(result)

    elif option == "🚆 Train Live Status":
        st.subheader("📍 Check Live Train Status")
        train_number = st.text_input("Enter Train Number:")
        if st.button("Get Train Status"):
            with st.spinner("Fetching details..."):
                result = get_train_status(train_number)
                st.success(result)

    elif option == "🆔 PNR Status":
        st.subheader("🎟️ Check PNR Status")
        pnr_number = st.text_input("Enter PNR Number:")
        if st.button("Get PNR Status"):
            with st.spinner("Fetching details..."):
                result = get_pnr_status(pnr_number)
                st.success(result)

    elif option == "💰 Train Fare":
        st.subheader("💸 Get Train Fare Details")
        col1, col2, col3 = st.columns(3)
        with col1:
            train_number = st.text_input("Enter Train Number:")
        with col2:
            source = st.text_input("From Station Code:")
        with col3:
            destination = st.text_input("To Station Code:")

        if st.button("Get Fare Details"):
            with st.spinner("Fetching details..."):
                result = get_train_fare(train_number, source, destination)
                st.success(result)

# Run the app
if __name__ == "__main__":
    app()

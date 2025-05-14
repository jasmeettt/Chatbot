import streamlit as st
import requests
from rule_based_chatbot import app as chatbot_app  # Import the main chatbot module
from rule_based_chatbot import ticket_chatbot_app  # Import a new function for ticket-specific chatbot

# API Base URL (Ensure `api.py` is running)
API_URL = "http://127.0.0.1:5001"

# Sidebar Navigation
st.sidebar.title("🚆 QuickRail System")
page = st.sidebar.radio("📌 Navigate to:", ["🏠 Home", "🤖 Chatbot", "🎟️ Book a Ticket", "📍 Train Services"])

# Home Page
if page == "🏠 Home":
    st.title("🚆 Welcome to QuickRail")
    st.markdown("### Your one-stop solution for train ticket booking & railway information.")
    st.image("/workspaces/Chatbot/assets/DALL·E 2025-03-09 03.43.10 - A modern, tech-inspired banner for QuickRail, a futuristic train ticket booking platform. The design features a sleek, high-speed train with glowing b.webp", use_container_width=True)

# Chatbot Page (Now separate)
elif page == "🤖 Chatbot":
    st.title("💬 QuickRail Chatbot")
    st.markdown("### Ask me anything about trains, stations, bookings, and more!")
    # Only the chatbot should be active on this page
    def chatbot_page():
        chatbot_app()  # Use the chatbot module here for general queries

    chatbot_page()  # Run the chatbot for this page

# Book a Ticket Page
elif page == "🎟️ Book a Ticket":
    st.subheader("🎟️ Book Your Train Ticket")
    st.markdown("""
    Interact with the chatbot below to assist you in booking a ticket. The chatbot will guide you through the necessary steps for booking your ticket.
    """)
    
    # Use a different function (ticket-specific chatbot logic) for booking
    def ticket_booking_chatbot_page():
        ticket_chatbot_app()  # This function will be used for ticket-related queries

    ticket_booking_chatbot_page()  # Run the ticket-specific chatbot for this page

# Train Services Page
elif page == "📍 Train Services":
    option = st.sidebar.radio("🔍 Select an option:", ["🏢 Station Details", "🚆 Train Live Status", "🆔 PNR Status", "💰 Train Fare"])

    # 🚉 Function to Fetch Station Details
    def get_station_details(station_code):
        response = requests.get(f"{API_URL}/station/{station_code}")
        if response.status_code == 200:
            return response.json().get("station_details", {})
        return None

    # 🚆 Function to Fetch Train Live Status
    def get_train_status(train_number):
        response = requests.get(f"{API_URL}/train_status/{train_number}")
        if response.status_code == 200:
            return response.json().get("train_status", {})
        return None

    # 🆔 Function to Fetch PNR Status
    def get_pnr_status(pnr_number):
        response = requests.get(f"{API_URL}/pnr_status/{pnr_number}")
        if response.status_code == 200:
            return response.json().get("pnr_status", {})
        return None

    # 💰 Function to Fetch Train Fare
    def get_train_fare(train_number, from_station, to_station, class_type, quota):
        params = {
            "train_number": train_number,
            "from": from_station,
            "to": to_station,
            "class": class_type,
            "quota": quota
        }
        response = requests.get(f"{API_URL}/train_fare", params=params)
        if response.status_code == 200:
            return response.json().get("train_fare", None)
        return None

    # 🚉 Station Details UI
    if option == "🏢 Station Details":
        st.subheader("🔎 Search for Station Details")
        station_code = st.text_input("Enter Station Code:")
        if st.button("Get Station Details"):
            with st.spinner("Fetching details..."):
                result = get_station_details(station_code)
                if isinstance(result, dict) and "name" in result:
                    st.markdown(f"""
                    ### 🚉 {result['name']}
                    - **Station Code:** `{result['code']}`
                    """)
                else:
                    st.error("❌ No station found!")

    # 🚆 Train Live Status UI
    elif option == "🚆 Train Live Status":
        st.subheader("📍 Check Live Train Status")
        train_number = st.text_input("Enter Train Number:")
        if st.button("Get Train Status"):
            with st.spinner("Fetching details..."):
                result = get_train_status(train_number)
                if isinstance(result, dict) and "name" in result:
                    st.markdown(f"""
                    ### 🚆 {result['name']}
                    - **Train Number:** `{train_number}`
                    - **Current Status:** `{result['status']}`
                    """)
                else:
                    st.error("❌ No train status found!")

    # 🆔 PNR Status UI
    elif option == "🆔 PNR Status":
        st.subheader("🔍 Check PNR Status")
        pnr_number = st.text_input("Enter PNR Number:")
        if st.button("Get PNR Status"):
            with st.spinner("Fetching details..."):
                result = get_pnr_status(pnr_number)
                if isinstance(result, dict) and "status" in result:
                    st.markdown(f"""
                    ### 🆔 PNR Status
                    - **Current Status:** `{result['status']}`
                    - **Seat Details:** `{result['seat']}`
                    """)
                else:
                    st.error("❌ No PNR details found!")

    # 💰 Train Fare UI
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
                if isinstance(result, int):
                    st.success(f"### 💰 Fare: ₹{result}")
                else:
                    st.error("❌ No fare details found!")

st.markdown("---")
st.markdown("💡 *Powered by QuickRail API* 🚀")

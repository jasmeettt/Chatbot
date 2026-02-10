import streamlit as st
import requests
from rule_based_chatbot import app as chatbot_app
from rule_based_chatbot import ticket_chatbot_app
from rule_based_chatbot import STATIONS, TRAINS, CHAT_CSS

# Page config
st.set_page_config(
    page_title="QuickRail — Train Booking & Info",
    page_icon="🚆",
    layout="wide"
)

# Inject custom CSS
st.markdown(CHAT_CSS, unsafe_allow_html=True)

# API Base URL
API_URL = "http://127.0.0.1:5001"

# --- Sidebar Navigation ---
st.sidebar.markdown("## 🚆 QuickRail")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "📌 Navigate to:",
    ["🏠 Home", "🤖 Chatbot", "🎟️ Book a Ticket", "📍 Train Services"],
    label_visibility="collapsed"
)

# =============================
# 🏠 Home Page
# =============================
if page == "🏠 Home":
    st.title("🚆 Welcome to QuickRail")
    st.markdown("### Your one-stop solution for train ticket booking & railway information.")

    # Try loading the banner image
    try:
        st.image("assets/DALL·E 2025-03-09 03.43.10 - A modern, tech-inspired banner for QuickRail, a futuristic train ticket booking platform. The design features a sleek, high-speed train with glowing b.webp", use_container_width=True)
    except Exception:
        st.info("🖼️ Banner image not found in `assets/` folder.")

    st.markdown("---")

    # Feature highlights
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("#### 🤖 Chatbot")
        st.caption("Ask about trains, stations, fares, and PNR status.")
    with col2:
        st.markdown("#### 🎟️ Book Tickets")
        st.caption("Step-by-step guided ticket booking with PDF download.")
    with col3:
        st.markdown("#### 📍 Live Status")
        st.caption("Real-time train status and PNR tracking.")
    with col4:
        st.markdown("#### 💰 Fare Check")
        st.caption("Compare fares across SL, 3A, 2A, and 1A classes.")

    st.markdown("---")

    # Quick start guide
    st.markdown("### 🚀 Get Started")
    st.info("👈 Use the **sidebar** to navigate between Chatbot, Booking, and Train Services.")

# =============================
# 🤖 Chatbot Page
# =============================
elif page == "🤖 Chatbot":
    chatbot_app()

# =============================
# 🎟️ Book a Ticket Page
# =============================
elif page == "🎟️ Book a Ticket":
    st.title("🎟️ Book Your Train Ticket")
    st.markdown("The chatbot will guide you step-by-step through the booking process.")
    st.markdown("---")
    ticket_chatbot_app()

# =============================
# 📍 Train Services Page
# =============================
elif page == "📍 Train Services":
    st.title("📍 Train Services")

    tab1, tab2, tab3, tab4 = st.tabs(["🏢 Station Details", "🚆 Train Status", "🆔 PNR Status", "💰 Train Fare"])

    # --- Station Details ---
    with tab1:
        st.subheader("🔎 Search for Station Details")
        station_options = [f"{code} — {name}" for code, name in STATIONS.items()]
        selected_station = st.selectbox(
            "Select or search for a station:",
            options=station_options,
            index=None,
            placeholder="Start typing a station name or code..."
        )

        if st.button("Get Station Details", use_container_width=True) and selected_station:
            station_code = selected_station.split(" — ")[0]
            with st.spinner("Fetching details..."):
                try:
                    response = requests.get(f"{API_URL}/station/{station_code}", timeout=5)
                    if response.status_code == 200:
                        result = response.json().get("station_details", {})
                        if isinstance(result, dict) and "name" in result:
                            st.success(f"### 🚉 {result['name']}")
                            st.markdown(f"- **Station Code:** `{result['code']}`")
                        else:
                            st.error("❌ Station not found!")
                    else:
                        st.error("❌ Station not found! Please check the code.")
                except requests.exceptions.ConnectionError:
                    st.error("⚠️ Cannot connect to API. Ensure `api.py` is running.")

    # --- Train Live Status ---
    with tab2:
        st.subheader("📍 Check Live Train Status")
        train_options = [f"{num} — {name}" for num, name in TRAINS.items()]
        selected_train = st.selectbox(
            "Select or search for a train:",
            options=train_options,
            index=None,
            placeholder="Start typing a train number or name..."
        )

        if st.button("Get Train Status", use_container_width=True) and selected_train:
            train_number = selected_train.split(" — ")[0]
            with st.spinner("Fetching status..."):
                try:
                    response = requests.get(f"{API_URL}/train_status/{train_number}", timeout=5)
                    if response.status_code == 200:
                        result = response.json().get("train_status", {})
                        if isinstance(result, dict) and "name" in result:
                            st.success(f"### 🚆 {result['name']}")
                            st.markdown(f"- **Train Number:** `{train_number}`")
                            st.markdown(f"- **Current Status:** `{result['status']}`")
                        else:
                            st.error(f"❌ No status found for train {train_number}!")
                    else:
                        st.error(f"❌ No status found for train {train_number}!")
                except requests.exceptions.ConnectionError:
                    st.error("⚠️ Cannot connect to API. Ensure `api.py` is running.")

    # --- PNR Status ---
    with tab3:
        st.subheader("🔍 Check PNR Status")
        pnr_number = st.text_input("Enter 10-digit PNR Number:", placeholder="e.g., 1234567890", max_chars=10)

        if st.button("Get PNR Status", use_container_width=True) and pnr_number:
            if len(pnr_number) != 10 or not pnr_number.isdigit():
                st.warning("⚠️ PNR must be exactly 10 digits.")
            else:
                with st.spinner("Fetching PNR details..."):
                    try:
                        response = requests.get(f"{API_URL}/pnr_status/{pnr_number}", timeout=5)
                        if response.status_code == 200:
                            result = response.json().get("pnr_status", {})
                            if isinstance(result, dict) and "status" in result:
                                st.success("### 🆔 PNR Status")
                                st.markdown(f"- **Current Status:** `{result['status']}`")
                                st.markdown(f"- **Seat Details:** `{result['seat']}`")
                            else:
                                st.error("❌ No PNR details found!")
                        else:
                            st.error("❌ No PNR details found!")
                    except requests.exceptions.ConnectionError:
                        st.error("⚠️ Cannot connect to API. Ensure `api.py` is running.")

    # --- Train Fare ---
    with tab4:
        st.subheader("💰 Check Train Fare")
        fare_train_options = [f"{num} — {name}" for num, name in TRAINS.items()]
        selected_fare_train = st.selectbox(
            "Select Train:",
            options=fare_train_options,
            index=None,
            placeholder="Choose a train...",
            key="fare_train"
        )
        class_type = st.selectbox("Select Class:", ["SL — Sleeper", "3A — AC 3 Tier", "2A — AC 2 Tier", "1A — AC First Class"])
        class_code = class_type.split(" — ")[0]

        if st.button("Get Train Fare", use_container_width=True) and selected_fare_train:
            train_number = selected_fare_train.split(" — ")[0]
            with st.spinner("Fetching fare..."):
                try:
                    params = {"train_number": train_number, "class": class_code}
                    response = requests.get(f"{API_URL}/train_fare", params=params, timeout=5)
                    if response.status_code == 200:
                        result = response.json().get("train_fare", None)
                        if isinstance(result, int):
                            st.success(f"### 💰 Fare: ₹{result}")
                            st.caption(f"Train {train_number} • Class {class_code}")
                        else:
                            st.error("❌ No fare details found!")
                    else:
                        st.error("❌ No fare details found!")
                except requests.exceptions.ConnectionError:
                    st.error("⚠️ Cannot connect to API. Ensure `api.py` is running.")

# --- Footer ---
st.markdown('<div class="footer-bar">💡 Powered by QuickRail API 🚀</div>', unsafe_allow_html=True)

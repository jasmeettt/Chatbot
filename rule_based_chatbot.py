import streamlit as st
import time
import json
import requests
import base64
from fpdf import FPDF
from datetime import datetime

from streamlit_lottie import st_lottie

# API Base URL
API_BASE_URL = "http://127.0.0.1:5001"

# Station data (synced with api.py)
STATIONS = {
    "NDLS": "New Delhi", "MMCT": "Mumbai Central", "HWH": "Howrah Junction",
    "CSMT": "CST Mumbai", "SBC": "Bangalore City", "MAS": "Chennai Central",
    "BBS": "Bhubaneswar", "PUNE": "Pune Junction", "JAT": "Jammu Tawi",
    "ADI": "Ahmedabad", "TNA": "Thane", "KYN": "Kalyan Junction",
    "PNVL": "Panvel", "DDR": "Dadar", "BVI": "Borivali",
    "VR": "Virar", "BUD": "Badlapur", "KJT": "Karjat",
    "LNL": "Lonavala", "CCH": "Chinchvad"
}

# Train data (synced with api.py)
TRAINS = {
    "12431": "Rajdhani Express", "11027": "Mumbai Mail",
    "12625": "Kerala Express", "12295": "Sanghamitra Express",
    "12951": "Mumbai Rajdhani", "12301": "Howrah Rajdhani",
    "12622": "Tamil Nadu Express", "12701": "AP Express",
    "12839": "Chennai Howrah Mail", "22120": "Tejas Express"
}

# Suggested prompts for the chatbot
SUGGESTED_PROMPTS = [
    {"label": "🚆 Train Status", "query": "status 12951"},
    {"label": "🎫 Check PNR", "query": "pnr 1234567890"},
    {"label": "🎟️ Book Ticket", "query": "book ticket"},
    {"label": "💰 Check Fare", "query": "fare 12431 sl"},
    {"label": "🏙️ Station Info", "query": "ndls"},
    {"label": "❓ Help", "query": "help"},
]

# Custom CSS for premium chat UI (contrast-safe for light & dark modes)
CHAT_CSS = """
<style>
    .welcome-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        padding: 24px;
        border-radius: 16px;
        margin: 16px 0;
        text-align: center;
    }
    .welcome-box h2 { color: white !important; margin: 0 0 8px 0; }
    .welcome-box p { color: rgba(255,255,255,0.9) !important; margin: 0; font-size: 1.05em; }

    .stat-card {
        background-color: rgba(100, 100, 100, 0.1);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        border: 1px solid rgba(150, 150, 150, 0.3);
    }
    .stat-card h3 { margin: 0; font-size: 1.4em; }
    .stat-card p { margin: 4px 0 0 0; opacity: 0.7; font-size: 0.9em; }

    .footer-bar {
        text-align: center;
        opacity: 0.5;
        font-size: 0.85em;
        padding: 12px 0;
        border-top: 1px solid rgba(150, 150, 150, 0.3);
        margin-top: 24px;
    }
</style>
"""


# Load animations
def load_lottie_animation(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

animation1 = load_lottie_animation("assets/quic_rail.json")
animation2 = load_lottie_animation("assets/payment_success.json")


# Session State Initialization
def init_state():
    keys_defaults = {
        "step": None, "messages": [], "num_passengers": None,
        "from_station": None, "to_station": None,
        "train": None, "class_type": None, "total_price": None,
        "show_payment": False, "show_thank_you": False, "payment_method": None
    }
    for key, default in keys_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default


# Reset session state after booking
def reset_booking():
    booking_keys = ["step", "num_passengers", "from_station", "to_station",
                    "train", "class_type", "total_price", "show_payment",
                    "show_thank_you", "payment_method"]
    for key in booking_keys:
        if key in st.session_state:
            st.session_state[key] = None
    st.session_state.show_payment = False
    st.session_state.show_thank_you = False


# PDF ticket generation
def generate_ticket_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "QuickRail - Ticket Confirmation", ln=True, align="C")

    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, f"Train Number: {st.session_state.train}", ln=True)
    pdf.cell(200, 10, f"Class: {st.session_state.class_type}", ln=True)
    pdf.cell(200, 10, f"No. of Passengers: {st.session_state.num_passengers}", ln=True)
    pdf.cell(200, 10, f"Total Fare: Rs. {st.session_state.total_price}", ln=True)
    pdf.cell(200, 10, "Payment Status: Successful", ln=True)
    pdf.cell(200, 10, "Have a safe journey!", ln=True)
    pdf.cell(200, 10, f"Issue Date: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", ln=True, align="R")

    file_path = "ticket.pdf"
    pdf.output(file_path)

    with open(file_path, "rb") as f:
        pdf_bytes = f.read()
    b64_pdf = base64.b64encode(pdf_bytes).decode()
    return f'<a href="data:application/pdf;base64,{b64_pdf}" download="QuickRail_Ticket.pdf">📥 Download Ticket PDF</a>'


# Rule-based chatbot logic
def get_chatbot_response(user_input):
    user_input_lower = user_input.lower().strip()

    if "book ticket" in user_input_lower or "book my ticket" in user_input_lower:
        return "🎟️ Sure! Please navigate to the **🎟️ Book a Ticket** page from the sidebar to start booking."

    if "status" in user_input_lower and any(char.isdigit() for char in user_input_lower):
        train_number = ''.join(filter(str.isdigit, user_input_lower))
        try:
            response = requests.get(f"{API_BASE_URL}/train_status/{train_number}", timeout=5)
            if response.status_code == 200:
                data = response.json().get("train_status", {})
                if isinstance(data, dict):
                    return f"🚆 **Train:** {data.get('name', 'N/A')}\n\n📍 **Status:** {data.get('status', 'Not available')}"
        except requests.exceptions.ConnectionError:
            return "⚠️ Cannot connect to the API. Make sure `api.py` is running."
        return f"❌ No status found for train **{train_number}**."

    if "pnr" in user_input_lower and any(char.isdigit() for char in user_input_lower):
        pnr_number = ''.join(filter(str.isdigit, user_input_lower))
        if len(pnr_number) != 10:
            return "⚠️ PNR number must be exactly **10 digits**."
        try:
            response = requests.get(f"{API_BASE_URL}/pnr_status/{pnr_number}", timeout=5)
            if response.status_code == 200:
                data = response.json().get("pnr_status", {})
                if isinstance(data, dict):
                    return f"🎫 **PNR Status:** {data.get('status')}\n\n💺 **Seat:** {data.get('seat')}"
        except requests.exceptions.ConnectionError:
            return "⚠️ Cannot connect to the API. Make sure `api.py` is running."
        return f"❌ No details found for PNR **{pnr_number}**."

    # Station lookup
    for code, name in STATIONS.items():
        if code.lower() in user_input_lower or name.lower() in user_input_lower:
            try:
                response = requests.get(f"{API_BASE_URL}/station/{code}", timeout=5)
                if response.status_code == 200:
                    data = response.json().get("station_details", {})
                    return f"🏙️ **Station:** {data.get('name')} (`{data.get('code')}`)"
            except requests.exceptions.ConnectionError:
                return "⚠️ Cannot connect to the API. Make sure `api.py` is running."
            return f"❌ Could not retrieve details for station **{code}**."

    if "fare" in user_input_lower:
        words = user_input_lower.split()
        train_number = next((word for word in words if word.isdigit()), None)
        class_map = {"sl": "SL", "3a": "3A", "2a": "2A", "1a": "1A"}
        found_class = next((cls for cls in class_map if cls in user_input_lower), None)

        if train_number and found_class:
            try:
                params = {"train_number": train_number, "class": class_map[found_class]}
                response = requests.get(f"{API_BASE_URL}/train_fare", params=params, timeout=5)
                if response.status_code == 200:
                    fare = response.json().get("train_fare", "N/A")
                    return f"💰 **Fare for Train {train_number}** ({class_map[found_class]}): **₹{fare}**"
            except requests.exceptions.ConnectionError:
                return "⚠️ Cannot connect to the API. Make sure `api.py` is running."
            return "❌ Could not retrieve fare details."
        return "💡 **Tip:** Try something like: `fare 12431 sl`"

    responses = {
        "hi": "👋 Hello! How can I assist you today?",
        "hello": "👋 Hi there! What can I help you with?",
        "hey": "👋 Hey! Ready to help you with train info.",
        "bye": "👋 Goodbye! Have a great journey!",
        "thanks": "😊 You're welcome! Happy to help.",
        "thank you": "😊 You're welcome! Feel free to ask anything else.",
        "help": "📋 **Here's what I can do:**\n\n"
                "• **Train Status** — e.g., `status 12951`\n"
                "• **PNR Status** — e.g., `pnr 1234567890`\n"
                "• **Station Info** — e.g., `ndls` or `pune`\n"
                "• **Train Fare** — e.g., `fare 12431 sl`\n"
                "• **Book Ticket** — say `book ticket`",
    }

    return responses.get(user_input_lower,
        "🤖 I didn't understand that. Try asking about **train status**, **fare**, **PNR**, or **station info**.\n\n💡 Type **help** for a list of commands.")


# Render suggested prompt chips
def render_suggestions():
    """Render clickable suggestion chips that trigger chatbot queries."""
    st.markdown("##### 💡 Try asking:")
    cols = st.columns(len(SUGGESTED_PROMPTS))
    for i, prompt in enumerate(SUGGESTED_PROMPTS):
        with cols[i]:
            if st.button(prompt["label"], key=f"suggestion_{i}", use_container_width=True):
                st.session_state.messages.append({"content": prompt["query"], "is_user": True})
                bot_reply = get_chatbot_response(prompt["query"])
                st.session_state.messages.append({"content": bot_reply, "is_user": False})
                st.rerun()


# Render chat history using st.chat_message
def render_chat_history():
    """Display chat messages with proper styling."""
    for message in st.session_state.messages:
        if message["is_user"]:
            with st.chat_message("user"):
                st.markdown(message["content"])
        else:
            with st.chat_message("assistant", avatar="🚆"):
                st.markdown(message["content"])


# Fetch train status
def fetch_train_status(train_number):
    try:
        response = requests.get(f"{API_BASE_URL}/train_status/{train_number}", timeout=5)
        if response.status_code == 200:
            train_info = response.json().get("train_status", {})
            if isinstance(train_info, dict):
                return f"✅ **Train Name:** {train_info.get('name', 'Unknown')}\n\n✅ **Status:** {train_info.get('status', 'No info')}"
    except requests.exceptions.ConnectionError:
        return "⚠️ API is not reachable. Ensure `api.py` is running."
    return "❌ No train status found!"


# Fare calculation
def fetch_ticket_price(train_number, class_type, num_passengers):
    try:
        params = {"train_number": train_number, "class": class_type}
        response = requests.get(f"{API_BASE_URL}/train_fare", params=params, timeout=5)
        if response.status_code == 200:
            base_fare = response.json().get("train_fare", 0)
            if isinstance(base_fare, int):
                return base_fare * num_passengers
    except requests.exceptions.ConnectionError:
        pass
    return 0


# Ticket booking chatbot
def ticket_chatbot_app():
    init_state()
    st.markdown(CHAT_CSS, unsafe_allow_html=True)

    if animation1:
        st_lottie(animation1, height=180, key="animation1")

    # Thank you state
    if st.session_state.show_thank_you:
        st.success("🎉 Your ticket has been successfully booked! Safe travels! ✨")
        if animation2:
            st_lottie(animation2, height=200, key="success_animation")
        st.markdown(generate_ticket_pdf(), unsafe_allow_html=True)
        if st.button("🏠 Book Another Ticket", use_container_width=True):
            reset_booking()
            st.rerun()
        return

    # Payment state
    if st.session_state.show_payment:
        st.subheader("💳 Secure Payment")
        st.info(f"**Total Amount: ₹{st.session_state.total_price}**")
        payment_method = st.radio("Select Payment Method:",
                                  ["Credit/Debit Card", "UPI", "Net Banking", "Wallet"])

        if payment_method == "Credit/Debit Card":
            st.text_input("Card Number", max_chars=16, placeholder="1234 5678 9012 3456")
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Expiry Date", max_chars=5, placeholder="MM/YY")
            with col2:
                st.text_input("CVV", max_chars=3, type="password", placeholder="***")
            st.text_input("Cardholder Name", placeholder="Name on card")
        elif payment_method == "UPI":
            st.text_input("Enter UPI ID", placeholder="example@upi")
        elif payment_method == "Net Banking":
            st.selectbox("Select Bank", ["HDFC Bank", "ICICI Bank", "SBI", "Axis Bank", "Other"])
        elif payment_method == "Wallet":
            st.selectbox("Select Wallet", ["Paytm", "Google Pay", "PhonePe", "Amazon Pay"])

        if st.button(f"💰 Pay ₹{st.session_state.total_price}", use_container_width=True, type="primary"):
            with st.spinner("Processing payment..."):
                time.sleep(1.5)
            st.session_state.show_payment = False
            st.session_state.show_thank_you = True
            st.rerun()
        return

    # Chat history
    render_chat_history()

    # Booking flow
    if st.session_state.step is None:
        st.markdown("---")
        st.markdown("Click below to start booking your train ticket.")
        if st.button("🎟️ Start Booking", use_container_width=True, type="primary"):
            st.session_state.messages.append({"content": "How many passengers are traveling?", "is_user": False})
            st.session_state.step = 1
            st.rerun()

    elif st.session_state.step == 1:
        num = st.text_input("👥 Number of passengers:", placeholder="e.g., 2")
        if st.button("Next →", use_container_width=True) and num and num.isdigit() and int(num) > 0:
            st.session_state.num_passengers = int(num)
            st.session_state.messages.append({"content": f"{num} passenger(s)", "is_user": True})
            st.session_state.messages.append({"content": "Enter your train number.", "is_user": False})
            st.session_state.step = 2
            st.rerun()

    elif st.session_state.step == 2:
        train_number = st.selectbox(
            "🚆 Select Train:",
            options=list(TRAINS.keys()),
            format_func=lambda x: f"{x} — {TRAINS[x]}"
        )
        if st.button("Next →", use_container_width=True):
            st.session_state.train = train_number
            train_status = fetch_train_status(train_number)
            st.session_state.messages.append({"content": f"Train {train_number} — {TRAINS.get(train_number, '')}", "is_user": True})
            st.session_state.messages.append({"content": train_status, "is_user": False})
            st.session_state.messages.append({"content": "Choose your travel class.", "is_user": False})
            st.session_state.step = 3
            st.rerun()

    elif st.session_state.step == 3:
        class_type = st.selectbox("Select Class:", ["SL — Sleeper", "3A — AC 3 Tier", "2A — AC 2 Tier", "1A — AC First Class"])
        class_code = class_type.split(" — ")[0]
        if st.button("Next →", use_container_width=True):
            st.session_state.class_type = class_code
            total_price = fetch_ticket_price(st.session_state.train, class_code, st.session_state.num_passengers)
            st.session_state.total_price = total_price
            st.session_state.messages.append({"content": f"Class: {class_type}", "is_user": True})
            st.session_state.messages.append({"content": f"💰 **Total Price: ₹{total_price}**", "is_user": False})
            st.session_state.messages.append({"content": "Ready to proceed to payment?", "is_user": False})
            st.session_state.step = 4
            st.rerun()

    elif st.session_state.step == 4:
        if st.button("💳 Proceed to Payment", use_container_width=True, type="primary"):
            st.session_state.show_payment = True
            st.rerun()


# General chatbot interface
def app():
    init_state()
    st.markdown(CHAT_CSS, unsafe_allow_html=True)

    # Welcome state when chat is empty
    if not st.session_state.messages:
        st.markdown("""
        <div class="welcome-box">
            <h2>👋 Welcome to QuickRail Chatbot</h2>
            <p>Ask me about train status, PNR, fares, stations, or start booking a ticket!</p>
        </div>
        """, unsafe_allow_html=True)

        # Quick stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="stat-card"><h3>{len(STATIONS)}</h3><p>Stations</p></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="stat-card"><h3>{len(TRAINS)}</h3><p>Trains</p></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="stat-card"><h3>4</h3><p>Classes</p></div>', unsafe_allow_html=True)

        st.markdown("")
        render_suggestions()

    else:
        # Render chat history
        render_chat_history()
        # Show suggestions below the chat
        with st.expander("💡 Suggested Prompts", expanded=False):
            render_suggestions()

    # Chat input
    user_input = st.chat_input("Type your question here... (e.g., 'status 12951' or 'help')")

    if user_input:
        st.session_state.messages.append({"content": user_input, "is_user": True})
        bot_reply = get_chatbot_response(user_input)
        st.session_state.messages.append({"content": bot_reply, "is_user": False})
        st.rerun()


if __name__ == "__main__":
    app()

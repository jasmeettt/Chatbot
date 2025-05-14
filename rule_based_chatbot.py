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
        "step": None, "messages": [], "num_passengers": None, "from_station": None, "to_station": None,
        "train": None, "class_type": None, "total_price": None, "show_payment": False,
        "show_thank_you": False, "payment_method": None
    }
    for key, default in keys_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default

# Reset session state after booking
def reset_booking():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# PDF ticket generation
# PDF ticket generation
# Enhanced PDF ticket generation
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

    file_path = "/tmp/ticket.pdf"
    pdf.output(file_path)

    with open(file_path, "rb") as f:
        pdf_bytes = f.read()
    b64_pdf = base64.b64encode(pdf_bytes).decode()
    return f'<a href="data:application/pdf;base64,{b64_pdf}" download="QuickRail_Ticket.pdf">📥 Download Ticket PDF</a>'


# Rule-based chatbot logic
def get_chatbot_response(user_input):
    user_input = user_input.lower().strip()

    if "book ticket" in user_input or "book my ticket" in user_input:
        st.session_state.step = 1
        st.session_state.messages.append({"content": "Sure, let's start booking your ticket!", "is_user": False})
        return "Redirecting you to booking..."

    if "status" in user_input and any(char.isdigit() for char in user_input):
        train_number = ''.join(filter(str.isdigit, user_input))
        response = requests.get(f"{API_BASE_URL}/train_status/{train_number}")
        if response.status_code == 200:
            data = response.json().get("train_status", {})
            if isinstance(data, dict):
                return f"🚆 Train: {data.get('name', 'N/A')}\n📍 Status: {data.get('status', 'Not available')}"
        return "❌ Could not fetch train status. Please try again."

    if "pnr" in user_input and any(char.isdigit() for char in user_input):
        pnr_number = ''.join(filter(str.isdigit, user_input))
        response = requests.get(f"{API_BASE_URL}/pnr_status/{pnr_number}")
        if response.status_code == 200:
            data = response.json().get("pnr_status", {})
            if isinstance(data, dict):
                return f"🎫 PNR Status: {data.get('status')}, Seat: {data.get('seat')}"
        return "❌ Unable to fetch PNR status."

    for code in ["ndls", "csmt", "mmct", "sbc", "mas", "bbs", "pune"]:
        if code in user_input:
            response = requests.get(f"{API_BASE_URL}/station/{code.upper()}")
            if response.status_code == 200:
                data = response.json().get("station_details", {})
                return f"🏙️ Station: {data.get('name')} ({data.get('code')})"
            return "❌ Could not retrieve station information."

    if "fare" in user_input:
        words = user_input.split()
        train_number = next((word for word in words if word.isdigit()), None)
        class_map = {"sl": "SL", "3a": "3A", "2a": "2A", "1a": "1A"}
        found_class = next((cls for cls in class_map if cls in user_input), None)

        if train_number and found_class:
            params = {"train_number": train_number, "class": class_map[found_class]}
            response = requests.get(f"{API_BASE_URL}/train_fare", params=params)
            if response.status_code == 200:
                fare = response.json().get("train_fare", "N/A")
                return f"💰 Fare for Train {train_number} ({class_map[found_class]}): ₹{fare}"
            return "❌ Could not retrieve fare details."

    responses = {
        "hi": "Hello! How can I assist you today?",
        "hello": "Hi there! What can I help you with?",
        "bye": "Goodbye! Have a great day!",
        "help": "You can ask me about train status, fare, PNR status, station info, or say 'book ticket' to start booking."
    }

    return responses.get(user_input, "🤖 Sorry, I didn’t get that. You can ask about train status, fare, station info, PNR, or say 'book ticket'.")

# Fetch train status
def fetch_train_status(train_number):
    response = requests.get(f"{API_BASE_URL}/train_status/{train_number}")
    if response.status_code == 200:
        train_info = response.json().get("train_status", {})
        if isinstance(train_info, dict):
            return f"✅ **Train Name:** {train_info.get('name', 'Unknown')}\n✅ **Status:** {train_info.get('status', 'No info')}"
    return "❌ No train status found!"

# Fare calculation
def fetch_ticket_price(train_number, class_type, num_passengers):
    params = {"train_number": train_number, "class": class_type}
    response = requests.get(f"{API_BASE_URL}/train_fare", params=params)
    if response.status_code == 200:
        base_fare = response.json().get("train_fare", 0)
        return base_fare * num_passengers
    return 0

# Ticket booking chatbot
def ticket_chatbot_app():
    init_state()
    st.title("🚆 QuickRail - Train Ticket Booking Chatbot")
    st_lottie(animation1, height=210, key="animation1")

    if st.session_state.show_thank_you:
        st.success("🎉 Your ticket has been successfully booked! Safe travels! ✨")
        if animation2:
            st_lottie(animation2, height=200, key="success_animation")
        st.markdown(generate_ticket_pdf(), unsafe_allow_html=True)
        if st.button("🏠 Back to Home"):
            reset_booking()
            st.rerun()
        return

    if st.session_state.show_payment:
        st.subheader("💳 Secure Payment")
        payment_method = st.radio("Select Payment Method:", ["Credit/Debit Card", "UPI", "Net Banking", "Wallet"])

        if payment_method == "Credit/Debit Card":
            st.text_input("Card Number", max_chars=16)
            st.text_input("Expiry Date (MM/YY)", max_chars=5)
            st.text_input("CVV", max_chars=3, type="password")
            st.text_input("Cardholder Name")
        elif payment_method == "UPI":
            st.text_input("Enter UPI ID")
        elif payment_method == "Net Banking":
            st.selectbox("Select Bank", ["HDFC Bank", "ICICI Bank", "SBI", "Axis Bank", "Other"])
        elif payment_method == "Wallet":
            st.selectbox("Select Wallet", ["Paytm", "Google Pay", "PhonePe", "Amazon Pay"])

        if st.button("💰 Pay ₹{}".format(st.session_state.total_price)):
            time.sleep(1.5)
            st.session_state.show_payment = False
            st.session_state.show_thank_you = True
            st.rerun()
        return

    for msg in st.session_state.messages:
        role = "👤 You" if msg["is_user"] else "🤖 Bot"
        st.markdown(f"**{role}:** {msg['content']}")

    if st.session_state.step is None:
        if st.button("🎟️ Start Booking"):
            st.session_state.messages.append({"content": "How many passengers are traveling?", "is_user": False})
            st.session_state.step = 1
            st.rerun()

    elif st.session_state.step == 1:
        num = st.text_input("👥 Enter number of passengers:")
        if st.button("Send") and num and num.isdigit():
            st.session_state.num_passengers = int(num)
            st.session_state.messages.append({"content": num, "is_user": True})
            st.session_state.messages.append({"content": "Enter your train number.", "is_user": False})
            st.session_state.step = 2
            st.rerun()

    elif st.session_state.step == 2:
        train_number = st.text_input("🚆 Enter Train Number:")
        if st.button("Send") and train_number:
            st.session_state.train = train_number
            train_status = fetch_train_status(train_number)
            st.session_state.messages.append({"content": train_number, "is_user": True})
            st.session_state.messages.append({"content": train_status, "is_user": False})
            st.session_state.messages.append({"content": "Choose class: SL, 3A, 2A, or 1A", "is_user": False})
            st.session_state.step = 3
            st.rerun()

    elif st.session_state.step == 3:
        class_type = st.selectbox("Select Class:", ["SL", "3A", "2A", "1A"])
        if st.button("Send"):
            st.session_state.class_type = class_type
            total_price = fetch_ticket_price(st.session_state.train, class_type, st.session_state.num_passengers)
            st.session_state.total_price = total_price
            st.session_state.messages.append({"content": f"Total Price: ₹{total_price}", "is_user": False})
            st.session_state.messages.append({"content": "Proceed to payment?", "is_user": False})
            st.session_state.step = 4
            st.rerun()

    elif st.session_state.step == 4:
        if st.button("💳 Proceed to Payment"):
            st.session_state.show_payment = True
            st.rerun()

# General chatbot interface
def app():
    init_state()
    st.title("🤖 QuickRail General Chatbot")
    st.markdown("Ask me anything about trains, ticket booking, or fares.")

    for message in st.session_state.messages:
        role = "👤 You" if message["is_user"] else "🤖 Bot"
        st.markdown(f"**{role}:** {message['content']}")

    user_input = st.chat_input("Type your question here...")

    if user_input:
        st.session_state.messages.append({"content": user_input, "is_user": True})
        bot_reply = get_chatbot_response(user_input)
        st.session_state.messages.append({"content": bot_reply, "is_user": False})
        st.rerun()

if __name__ == "__main__":
    app()

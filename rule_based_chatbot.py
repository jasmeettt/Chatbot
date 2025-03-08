import streamlit as st
import time
import json
import requests
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

# Initialize session state
def init_state():
    for key in ["step", "messages", "num_passengers", "from_station", "to_station", "train", "class_type", "total_price", "show_payment", "show_thank_you", "payment_method"]:
        if key not in st.session_state:
            st.session_state[key] = None
    if st.session_state.messages is None:
        st.session_state.messages = []

def reset_booking():
    for key in ["step", "messages", "num_passengers", "from_station", "to_station", "train", "class_type", "total_price", "show_payment", "show_thank_you", "payment_method"]:
        st.session_state[key] = None
    st.session_state.messages = []

def fetch_train_status(train_number):
    response = requests.get(f"{API_BASE_URL}/train_status/{train_number}")
    if response.status_code == 200:
        train_info = response.json().get("train_status", {})
        if isinstance(train_info, dict):
            return f"✅ **Train Name:** {train_info.get('name', 'Unknown')}\n✅ **Status:** {train_info.get('status', 'No info')}"
    return "❌ No train status found!"

def fetch_ticket_price(train_number, class_type, num_passengers):
    params = {"train_number": train_number, "class": class_type}
    response = requests.get(f"{API_BASE_URL}/train_fare", params=params)
    if response.status_code == 200:
        base_fare = response.json().get("train_fare", 0)
        return base_fare * num_passengers
    return 0

def app():
    init_state()
    st.title("🚆 QuickRail - Train Ticket Booking Chatbot")
    st_lottie(animation1, height=210, key="animation1")
    
    if st.session_state.show_thank_you:
        st.success("🎉 Your ticket has been successfully booked! Safe travels! ✨")
        if animation2:
            st_lottie(animation2, height=200, key="success_animation")
        if st.button("🏠 Back to Home"):
            reset_booking()
            st.rerun()
        return
    
    if st.session_state.show_payment:
        st.subheader("💳 Secure Payment")
        payment_method = st.radio("Select Payment Method:", ["Credit/Debit Card", "UPI", "Net Banking", "Wallet"])
        
        if payment_method == "Credit/Debit Card":
            card_number = st.text_input("Card Number", max_chars=16)
            expiry = st.text_input("Expiry Date (MM/YY)", max_chars=5)
            cvv = st.text_input("CVV", max_chars=3, type="password")
            card_name = st.text_input("Cardholder Name")
        elif payment_method == "UPI":
            upi_id = st.text_input("Enter UPI ID")
        elif payment_method == "Net Banking":
            bank = st.selectbox("Select Bank", ["HDFC Bank", "ICICI Bank", "SBI", "Axis Bank", "Other"])
        elif payment_method == "Wallet":
            wallet = st.selectbox("Select Wallet", ["Paytm", "Google Pay", "PhonePe", "Amazon Pay"])
        
        if st.button("💰 Pay ₹{}".format(st.session_state.total_price)):
            time.sleep(1.5)
            st.session_state.show_payment = False
            st.session_state.show_thank_you = True
            st.rerun()
        return
    
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            if msg["is_user"]:
                st.markdown(f"👤 **You:** {msg['content']}")
            else:
                st.markdown(f"🤖 **Bot:** {msg['content']}")
    
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

if __name__ == "__main__":
    app()
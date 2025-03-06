import streamlit as st
import time
import json
from streamlit_lottie import st_lottie

# ---------- Utility Functions ----------

def load_lottie_animation(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

animation1 = load_lottie_animation("assets/quic_rail.json")

# Define modern icons for bot and user
BOT_AVATAR = "🤖"
USER_AVATAR = "👤"

# Define stations and train details
stations = ["Bangalore", "Delhi", "Mumbai", "Chennai", "Hyderabad", "Kolkata", "Jaipur"]
trains = {
    ("Bangalore", "Delhi"): {"train": "Rajdhani Express", "number": "12431", "timing": "06:00 AM", "sleeper": 800, "ac": 2000},
    ("Mumbai", "Chennai"): {"train": "Mumbai Mail", "number": "11027", "timing": "08:30 PM", "sleeper": 700, "ac": 1800},
    ("Kolkata", "Hyderabad"): {"train": "Falaknuma Express", "number": "12704", "timing": "04:45 PM", "sleeper": 750, "ac": 1900},
}

# ---------- Session State Initialization ----------

def init_state():
    if "step" not in st.session_state:
        st.session_state.step = 0
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "num_passengers" not in st.session_state:
        st.session_state.num_passengers = None
    if "from_station" not in st.session_state:
        st.session_state.from_station = None
    if "to_station" not in st.session_state:
        st.session_state.to_station = None
    if "show_qr" not in st.session_state:
        st.session_state.show_qr = False
    if "show_thank_you" not in st.session_state:
        st.session_state.show_thank_you = False
    if "selected_class" not in st.session_state:
        st.session_state.selected_class = None

def reset_booking():
    st.session_state.step = 0
    st.session_state.messages = []
    st.session_state.num_passengers = None
    st.session_state.from_station = None
    st.session_state.to_station = None
    st.session_state.selected_class = None
    st.session_state.show_qr = False
    st.session_state.show_thank_you = False

# ---------- Main App Function ----------

def app():
    init_state()
    
    st.title("🚆 QuickRail - Train Ticket Booking Chatbot")
    st_lottie(animation1, height=210, key="animation1")
    
    # If payment is done, show a Thank You message & button to reset the flow.
    if st.session_state.show_thank_you:
        st.success("\U0001f39f️ Your tickets have been booked successfully! Have a safe journey! ✨")
        if st.button("🎉 Thank You", key="thank_you"):
            reset_booking()
            st.rerun()
        return
    
    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            st.chat_message("assistant" if not msg["is_user"] else "user").markdown(msg["content"])
    
    # Step 0: Start booking process
    if st.session_state.step == 0:
        if st.button("🎟️ Book your Tickets Now", key="start_booking"):
            st.session_state.messages.append({"content": "Hello! 👋 How many passengers are traveling?", "is_user": False})
            st.session_state.step = 1
            st.rerun()
    
    # Step 1: Number of passengers
    if st.session_state.step == 1:
        num = st.selectbox("👥 Number of passengers:", list(range(1, 11)), key="passenger_select")
        if st.button("✅ Submit", key="passenger_submit"):
            st.session_state.num_passengers = num
            st.session_state.messages.append({"content": str(num), "is_user": True})
            st.session_state.messages.append({"content": "📍 Please select your departure station.", "is_user": False})
            st.session_state.step = 2
            st.rerun()
    
    # Step 2: Departure station
    elif st.session_state.step == 2:
        dep = st.selectbox("🚉 Departure station:", stations, key="departure_select")
        if st.button("✅ Submit", key="departure_submit"):
            st.session_state.from_station = dep
            st.session_state.messages.append({"content": dep, "is_user": True})
            st.session_state.messages.append({"content": "🎯 Please select your destination station.", "is_user": False})
            st.session_state.step = 3
            st.rerun()
    
    # Step 3: Destination station
    elif st.session_state.step == 3:
        dest = st.selectbox("🎯 Destination station:", stations, key="destination_select")
        if dest == st.session_state.from_station:
            st.error("❌ Departure and destination stations cannot be the same!")
        else:
            if st.button("✅ Submit", key="destination_submit"):
                st.session_state.to_station = dest
                st.session_state.messages.append({"content": dest, "is_user": True})
                st.session_state.messages.append({"content": "🛏️ Select your class: Sleeper or AC", "is_user": False})
                st.session_state.step = 4
                st.rerun()
    
    # Step 4: Select Class
    elif st.session_state.step == 4:
        train_info = trains.get((st.session_state.from_station, st.session_state.to_station), None)
        if train_info:
            selected_class = st.radio("🎟️ Choose Class:", ("Sleeper", "AC"), key="class_select")
            if st.button("✅ Submit", key="class_submit"):
                st.session_state.selected_class = selected_class
                price = train_info["sleeper"] if selected_class == "Sleeper" else train_info["ac"]
                total_price = st.session_state.num_passengers * price
                st.session_state.messages.append({"content": f"💰 Your total price is ₹{total_price} for {selected_class} class on {train_info['train']} ({train_info['number']}) at {train_info['timing']}", "is_user": False})
                st.session_state.step = 5
                st.rerun()

# Step 5: Payment with QR overlay
    elif st.session_state.step == 5:
        if st.button("💳 Make Payment", key="payment"):
            st.session_state.show_qr = True
            st.image("assets/payment.jpg")
            st.rerun()
    
    # Show QR code overlay when payment is clicked
    if st.session_state.show_qr:
        st.markdown(
            """
            <style>
            .overlay {
                position: fixed;
                top: 0; left: 0;
                width: 100%; height: 100%;
                background: rgba(0, 0, 0, 0.6);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 1000;
            }
            .modal {
                background: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
            }
            </style>
            <div class='overlay'>
                <div class='modal'>
                    <h3>Scan QR to Pay</h3>
                    <img src='assets/payment.jpg' width='250'>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        time.sleep(3)
        st.session_state.show_qr = False
        st.session_state.show_thank_you = True
        st.rerun()
if __name__ == "__main__":
    app()

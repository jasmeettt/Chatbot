import streamlit as st
import json
from streamlit_lottie import st_lottie

# ---------- Utility Functions ----------

def load_lottie_animation(file_path):
    """Load Lottie animations from a JSON file."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None  # Avoid errors if the file is missing

# Load animations
animation1 = load_lottie_animation("assets/quic_rail.json")
animation2 = load_lottie_animation("assets/payment_success.json")  # Success animation

# Define available stations and train details
stations = ["Bangalore", "Delhi", "Mumbai", "Chennai", "Hyderabad", "Kolkata", "Jaipur"]

trains = {
    ("Bangalore", "Delhi"): {
        "train": "Rajdhani Express", "number": "12431", "timing": "06:00 AM",
        "sleeper": 800, "ac": 2000, "duration": "36h", "stops": ["Nagpur", "Bhopal", "Agra"],
        "coaches": 20
    },
    ("Mumbai", "Chennai"): {
        "train": "Mumbai Mail", "number": "11027", "timing": "08:30 PM",
        "sleeper": 700, "ac": 1800, "duration": "24h", "stops": ["Pune", "Solapur", "Vellore"],
        "coaches": 18
    },
    ("Kolkata", "Hyderabad"): {
        "train": "Falaknuma Express", "number": "12704", "timing": "04:45 PM",
        "sleeper": 750, "ac": 1900, "duration": "26h", "stops": ["Bhubaneswar", "Vijayawada"],
        "coaches": 22
    },
    ("Delhi", "Chennai"): {
        "train": "Tamil Nadu Express", "number": "12622", "timing": "06:30 PM",
        "sleeper": 1000, "ac": 2500, "duration": "32h", "stops": ["Nagpur", "Bhopal", "Vijayawada"],
        "coaches": 24
    },
    ("Bangalore", "Hyderabad"): {
        "train": "Kacheguda Express", "number": "12786", "timing": "10:00 PM",
        "sleeper": 600, "ac": 1500, "duration": "10h", "stops": ["Guntakal", "Kurnool"],
        "coaches": 16
    }
}

# ---------- Session State Initialization ----------

def init_state():
    """Initialize session state variables for chatbot flow."""
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
    if "show_payment" not in st.session_state:
        st.session_state.show_payment = False
    if "show_thank_you" not in st.session_state:
        st.session_state.show_thank_you = False
    if "selected_class" not in st.session_state:
        st.session_state.selected_class = None

def reset_booking():
    """Reset the chatbot flow and session state."""
    st.session_state.step = 0
    st.session_state.messages = []
    st.session_state.num_passengers = None
    st.session_state.from_station = None
    st.session_state.to_station = None
    st.session_state.selected_class = None
    st.session_state.show_payment = False
    st.session_state.show_thank_you = False

# ---------- Main App Function ----------

def app():
    init_state()
    
    # App title and animation
    st.title("🚆 QuickRail - Train Ticket Booking Chatbot")
    st_lottie(animation1, height=210, key="animation1")
    
    # If payment is done, show a Thank You message & reset button.
    if st.session_state.show_thank_you:
        st.success("🎉 Your tickets have been booked successfully! Have a safe journey! ✨")
        st.balloons()
        if animation2:
            st_lottie(animation2, height=200, key="success_animation")
        if st.button("🏠 Back to Home"):
            reset_booking()
            st.rerun()
        return

    # Display chat messages side by side
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            col1, col2 = st.columns([1, 1])
            if msg["is_user"]:
                with col2:
                    st.info(f"👤 {msg['content']}")
            else:
                with col1:
                    st.success(f"🤖 {msg['content']}")

    # Step 0: Start booking process
    if st.session_state.step == 0:
        if st.button("🎟️ Book your Tickets Now"):
            st.session_state.messages.append({"content": "Hello! 👋 How many passengers are traveling?", "is_user": False})
            st.session_state.step = 1
            st.rerun()

    # Step 1: Number of passengers
    elif st.session_state.step == 1:
        num = st.selectbox("👥 Number of passengers:", list(range(1, 11)))
        if st.button("✅ Submit"):
            st.session_state.num_passengers = num
            st.session_state.messages.append({"content": str(num), "is_user": True})
            st.session_state.messages.append({"content": "🚉 Please select your departure station.", "is_user": False})
            st.session_state.step = 2
            st.rerun()

    # Step 2: Departure station
    elif st.session_state.step == 2:
        dep = st.selectbox("🚉 Departure station:", stations)
        if st.button("✅ Submit"):
            st.session_state.from_station = dep
            st.session_state.messages.append({"content": dep, "is_user": True})
            st.session_state.messages.append({"content": "🎯 Please select your destination station.", "is_user": False})
            st.session_state.step = 3
            st.rerun()

    # Step 3: Destination station
    elif st.session_state.step == 3:
        dest = st.selectbox("🎯 Destination station:", stations)
        if dest == st.session_state.from_station:
            st.error("❌ Departure and destination stations cannot be the same!")
        else:
            if st.button("✅ Submit"):
                st.session_state.to_station = dest
                st.session_state.messages.append({"content": dest, "is_user": True})
                st.session_state.messages.append({"content": "🛏️ Select your class: Sleeper or AC", "is_user": False})
                st.session_state.step = 4
                st.rerun()

    # Step 4: Select Class
    elif st.session_state.step == 4:
        train_info = trains.get((st.session_state.from_station, st.session_state.to_station))
        if train_info:
            selected_class = st.radio("🎟️ Choose Class:", ("Sleeper", "AC"))
            if st.button("✅ Submit"):
                price = train_info[selected_class.lower()]
                total_price = st.session_state.num_passengers * price
                st.session_state.messages.append({
                    "content": f"🚆 **{train_info['train']}** ({train_info['number']})\n"
                               f"⏳ **Duration:** {train_info['duration']}\n"
                               f"🛑 **Stops:** {', '.join(train_info['stops'])}\n"
                               f"💺 **Coaches:** {train_info['coaches']}\n"
                               f"💰 **Total Price:** ₹{total_price}",
                    "is_user": False
                })
                st.session_state.messages.append({"content": "📲 Proceed to payment?", "is_user": False})
                st.session_state.step = 5
                st.rerun()

    # Step 5: Payment Page
    elif st.session_state.step == 5:
        st.image("assets/payment.jpg", caption="📸 Scan this QR code to complete your payment", width=300)
        if st.button("✅ Confirm Payment"):
            st.session_state.show_thank_you = True
            st.rerun()

# Run the app
if __name__ == "__main__":
    app()

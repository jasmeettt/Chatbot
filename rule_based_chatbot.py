import streamlit as st
import time
import json
from streamlit_lottie import st_lottie

#  Utility Functions 

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

stations = [
    "Bangalore", "Delhi", "Mumbai", "Chennai", "Hyderabad", "Kolkata", "Jaipur", 
    "Pune", "Ahmedabad", "Lucknow", "Patna", "Bhopal", "Indore", "Goa", "Surat"
]

trains = {
    # Existing Routes
    ("Bangalore", "Delhi"): {"train": "Rajdhani Express", "number": "12431", "timing": "06:00 AM", "sleeper": 800, "ac": 2000},
    ("Mumbai", "Chennai"): {"train": "Mumbai Mail", "number": "11027", "timing": "08:30 PM", "sleeper": 700, "ac": 1800},
    ("Kolkata", "Hyderabad"): {"train": "Falaknuma Express", "number": "12704", "timing": "04:45 PM", "sleeper": 750, "ac": 1900},
    ("Chennai", "Jaipur"): {"train": "Marudhar Express", "number": "14854", "timing": "07:15 AM", "sleeper": 900, "ac": 2100},
    ("Delhi", "Mumbai"): {"train": "Golden Temple Mail", "number": "12904", "timing": "09:30 PM", "sleeper": 850, "ac": 2050},
    ("Pune", "Ahmedabad"): {"train": "Shatabdi Express", "number": "12009", "timing": "05:30 AM", "sleeper": 750, "ac": 1900},
    ("Lucknow", "Delhi"): {"train": "Gomti Express", "number": "12419", "timing": "07:00 AM", "sleeper": 600, "ac": 1600},
    ("Hyderabad", "Bangalore"): {"train": "Kacheguda Express", "number": "17603", "timing": "06:45 PM", "sleeper": 850, "ac": 2000},
    ("Ahmedabad", "Jaipur"): {"train": "Ashram Express", "number": "12915", "timing": "09:45 PM", "sleeper": 900, "ac": 2200},
    ("Patna", "Delhi"): {"train": "Vaishali Express", "number": "12553", "timing": "05:50 PM", "sleeper": 700, "ac": 1850},
    ("Bhopal", "Mumbai"): {"train": "Punjab Mail", "number": "12138", "timing": "10:15 AM", "sleeper": 800, "ac": 1950},
    ("Goa", "Mumbai"): {"train": "Konkan Kanya Express", "number": "10111", "timing": "06:00 PM", "sleeper": 850, "ac": 2050},
    ("Surat", "Ahmedabad"): {"train": "Intercity Express", "number": "22953", "timing": "07:15 AM", "sleeper": 500, "ac": 1400},
    ("Indore", "Jaipur"): {"train": "Indore-Jaipur Express", "number": "12973", "timing": "11:30 AM", "sleeper": 750, "ac": 1800},
    ("Delhi", "Bangalore"): {"train": "Karnataka Express", "number": "12628", "timing": "08:20 PM", "sleeper": 900, "ac": 2200},
    ("Chennai", "Kolkata"): {"train": "Coromandel Express", "number": "12841", "timing": "02:50 PM", "sleeper": 950, "ac": 2300},
    ("Hyderabad", "Pune"): {"train": "Shatabdi Express", "number": "12026", "timing": "06:15 AM", "sleeper": 800, "ac": 1900},
    ("Pune", "Mumbai"): {"train": "Deccan Express", "number": "11238", "timing": "03:30 PM", "sleeper": 800, "ac": 1900},

}


# Session State Initialization 

def init_state():
    """Initialize session state variables for chatbot flow."""
    for key in ["step", "messages", "num_passengers", "from_station", "to_station", "show_payment", "show_thank_you", "selected_class"]:
        if key not in st.session_state:
            st.session_state[key] = None
    if st.session_state.messages is None:
        st.session_state.messages = []

def reset_booking():
    """Reset the chatbot flow and session state."""
    for key in ["step", "messages", "num_passengers", "from_station", "to_station", "show_payment", "show_thank_you", "selected_class"]:
        st.session_state[key] = None
    st.session_state.messages = []

# Main App Function 

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
    
    # Chat interface
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            cols = st.columns([1, 3, 1])  # Adjusted for better spacing
            if msg["is_user"]:
                with cols[2]:  # User messages on the right with more spacing
                    st.markdown(f"👤 **You:** {msg['content']}")
            else:
                with cols[0]:  # Bot messages on the left with better alignment
                    st.markdown(f"🤖 **Bot:** {msg['content']}")

    # Step 0: Start booking process
    if st.session_state.step is None:
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
        train_info = trains.get((st.session_state.from_station, st.session_state.to_station), None)
        if train_info:
            selected_class = st.selectbox("🎟️ Choose Class:", ["Sleeper", "AC"])  # Changed to selectbox
            if st.button("✅ Submit"):
                st.session_state.selected_class = selected_class
                price = train_info["sleeper"] if selected_class == "Sleeper" else train_info["ac"]
                total_price = st.session_state.num_passengers * price
                st.session_state.messages.append({
                    "content": f"💰 Your total price is **₹{total_price}** for **{selected_class} class** on **{train_info['train']} ({train_info['number']})** at **{train_info['timing']}**",
                    "is_user": False
                })
                st.session_state.messages.append({"content": "📲 Proceed to payment?", "is_user": False})
                st.session_state.step = 5
                st.rerun()
    
    # Step 5: Payment Page
    elif st.session_state.step == 5:
        st.subheader("💳 Secure Payment Portal")
        payment_method = st.radio("Choose Payment Method:", ["Credit/Debit Card", "UPI", "Net Banking", "Wallet"])
        if payment_method == "Credit/Debit Card":
            st.text_input("Card Number", placeholder="1234 5678 9012 3456")
            st.text_input("Expiry Date", placeholder="MM/YY")
            st.text_input("CVV", placeholder="***", type="password")
        elif payment_method == "UPI":
            st.text_input("Enter UPI ID", placeholder="yourname@upi")
        elif payment_method == "Net Banking":
            st.selectbox("Select Bank", ["SBI", "HDFC", "ICICI", "Axis", "Kotak"])
        elif payment_method == "Wallet":
            st.selectbox("Select Wallet", ["Paytm", "PhonePe", "Google Pay"])
        
        if st.button("✅ Confirm Payment"):
            st.session_state.show_thank_you = True
            st.rerun()

# Run the app
if __name__ == "__main__":
    app()

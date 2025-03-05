import streamlit as st
from streamlit_chat import message
import time
import json
from streamlit_lottie import st_lottie

# Utility to load a Lottie animation
def load_lottie_animation(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

animation1 = load_lottie_animation("assets/quic_rail.json")

# Define stations and pricing
stations = ["Banglore", "Delhi", "Mumbai", "Chennai", "Hyderabad", "Kolkata", "Jaipur"]

prices = {
    ("Banglore", "Delhi"): 20, ("Banglore", "Mumbai"): 30, ("Banglore", "Chennai"): 40,
    ("Banglore", "Hyderabad"): 25, ("Banglore", "Kolkata"): 35, ("Banglore", "Jaipur"): 35,
    ("Delhi", "Banglore"): 20, ("Delhi", "Mumbai"): 30, ("Delhi", "Chennai"): 40,
    ("Delhi", "Hyderabad"): 25, ("Delhi", "Kolkata"): 35, ("Delhi", "Jaipur"): 35,
    ("Mumbai", "Banglore"): 30, ("Mumbai", "Delhi"): 30, ("Mumbai", "Chennai"): 40,
    ("Mumbai", "Hyderabad"): 25, ("Mumbai", "Kolkata"): 35, ("Mumbai", "Jaipur"): 35,
    ("Chennai", "Banglore"): 40, ("Chennai", "Delhi"): 40, ("Chennai", "Mumbai"): 40,
    ("Chennai", "Hyderabad"): 25, ("Chennai", "Kolkata"): 35, ("Chennai", "Jaipur"): 35,
    ("Hyderabad", "Banglore"): 25, ("Hyderabad", "Delhi"): 25, ("Hyderabad", "Mumbai"): 25,
    ("Hyderabad", "Chennai"): 25, ("Hyderabad", "Kolkata"): 35, ("Hyderabad", "Jaipur"): 35,
    ("Kolkata", "Banglore"): 35, ("Kolkata", "Delhi"): 35, ("Kolkata", "Mumbai"): 35,
    ("Kolkata", "Chennai"): 35, ("Kolkata", "Hyderabad"): 35, ("Kolkata", "Jaipur"): 35,
    ("Jaipur", "Banglore"): 35, ("Jaipur", "Delhi"): 35, ("Jaipur", "Mumbai"): 35,
    ("Jaipur", "Chennai"): 35, ("Jaipur", "Hyderabad"): 35, ("Jaipur", "Kolkata"): 35,
}

def calculate_price(from_station, to_station, passengers):
    return prices.get((from_station, to_station), 50) * passengers

# Initialize session state variables if they don't exist
def initialize_session_state():
    if "step" not in st.session_state:
        st.session_state["step"] = 0
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "num_passengers" not in st.session_state:
        st.session_state["num_passengers"] = None
    if "from_station" not in st.session_state:
        st.session_state["from_station"] = None
    if "to_station" not in st.session_state:
        st.session_state["to_station"] = None
    if "show_thank_you" not in st.session_state:
        st.session_state["show_thank_you"] = False
    if "start_time" not in st.session_state:
        st.session_state["start_time"] = None

# Reset session state to start fresh
def reset_session_state():
    st.session_state["step"] = 0
    st.session_state["messages"] = []
    st.session_state["num_passengers"] = None
    st.session_state["from_station"] = None
    st.session_state["to_station"] = None
    st.session_state["show_thank_you"] = False
    st.session_state["start_time"] = None

def app():
    initialize_session_state()

    st.title("QuickRail - Train Ticket Booking Chatbot")
    st_lottie(animation1, height=210, key="animation1")
    
    # If the thank-you step is reached, show reset option and exit further processing.
    if st.session_state["show_thank_you"]:
        if st.button("Thank You", key="thank_you"):
            reset_session_state()
            st.rerun()
        return

    # Step 0: Start booking process
    if st.session_state["step"] == 0:
        if st.button("Book your Tickets Now", key="start"):
            st.session_state["messages"].append({
                "content": "Hello! How many passengers are traveling?",
                "is_user": False
            })
            st.session_state["step"] = 1
            st.rerun()

    # Display chat messages
    for msg in st.session_state["messages"]:
        role = "assistant" if not msg["is_user"] else "user"
        avatar = "train.png" if role == "assistant" else "user.jpg"
        with st.chat_message(role, avatar=avatar):
            st.write(msg["content"])

    # Step 1: Number of passengers
    if st.session_state["step"] == 1:
        user_input = st.selectbox("Number of passengers:", list(range(1, 11)), key="passenger_select")
        if st.button("Submit", key="passenger_submit"):
            st.session_state["num_passengers"] = user_input
            st.session_state["messages"].append({
                "content": f"{user_input}",
                "is_user": True
            })
            st.session_state["messages"].append({
                "content": "Please select your departure station.",
                "is_user": False
            })
            st.session_state["step"] = 2
            st.rerun()

    # Step 2: Departure station
    elif st.session_state["step"] == 2:
        user_input = st.selectbox("Departure station:", stations, key="departure_select")
        if st.button("Submit", key="departure_submit"):
            st.session_state["from_station"] = user_input
            st.session_state["messages"].append({
                "content": user_input,
                "is_user": True
            })
            st.session_state["messages"].append({
                "content": "Please select your destination station.",
                "is_user": False
            })
            st.session_state["step"] = 3
            st.rerun()

    # Step 3: Destination station
    elif st.session_state["step"] == 3:
        user_input = st.selectbox("Destination station:", stations, key="destination_select")
        if user_input == st.session_state["from_station"]:
            st.error("Departure and destination stations cannot be the same!")
        else:
            if st.button("Submit", key="destination_submit"):
                st.session_state["to_station"] = user_input
                st.session_state["messages"].append({
                    "content": user_input,
                    "is_user": True
                })
                ticket_price = calculate_price(
                    st.session_state["from_station"],
                    st.session_state["to_station"],
                    st.session_state["num_passengers"]
                )
                st.session_state["messages"].append({
                    "content": f"Your total price is ₹{ticket_price}.",
                    "is_user": False
                })
                st.session_state["step"] = 4
                st.rerun()

    # Step 4: Payment
    elif st.session_state["step"] == 4:
        if st.button("Make Payment", key="payment"):
            st.image("payment.jpg")
            time.sleep(5)
            st.session_state["show_thank_you"] = True
            st.rerun()

if __name__ == "__main__":
    app()

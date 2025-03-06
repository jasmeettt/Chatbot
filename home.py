import streamlit as st
import requests

# Function to fetch train station details from RapidAPI
def get_station_details(station_code):
    url = "https://irctc1.p.rapidapi.com/api/v1/searchStation"
    headers = {
        "x-rapidapi-key": "4d0dc103a0mshe97cfb09b21c167p12b446jsn8b5b922e8340",  # Replace with your API key
        "x-rapidapi-host": "irctc1.p.rapidapi.com"
    }
    querystring = {"query": station_code}

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        return response.json()  # Return station details as JSON
    else:
        return {"error": "Unable to fetch station details"}

# Chatbot Function
def chatbot_response(user_input):
    user_input = user_input.lower()

    # If user asks for train station details
    if user_input.startswith("station "):  # Example: "station BJU"
        station_code = user_input.split()[-1]  # Extract station code
        station_info = get_station_details(station_code)
        return f"Train Station Details: {station_info}"

    # Default chatbot responses
    responses = {
        "hi": "Hello! 👋 How can I assist you today?",
        "bye": "Goodbye! Have a great day! 😊",
        "what can you do": "I can chat with you, answer train queries, and keep you entertained! 🚆"
    }

    return responses.get(user_input, "I'm still learning! 😊")

# Streamlit UI
def app():
    st.title("Indian Railways Chatbot 🚆")
    
    gradient_text_html = """
        <style>
        .gradient-text {
            font-weight: bold;
            background: -webkit-linear-gradient(left, #07539e, #4fc3f7, #ffffff);
            background: linear-gradient(to right, #07539e, #4fc3f7, #ffffff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline;
            font-size: 3em;
        }
        </style>
        <div class="gradient-text">Welcome to The Chatbot </div>
        """

    st.markdown(gradient_text_html, unsafe_allow_html=True)
    
    st.markdown("#### 🤖 Chat with the Bot")
    user_input = st.text_input("💬 Type your message here:", key="user_input")

    if user_input:
        bot_reply = chatbot_response(user_input)
        st.write(f"🤖 **Bot:** {bot_reply}")
        st.rerun()  # Clears the input field after response

if __name__ == "__main__":
    app()

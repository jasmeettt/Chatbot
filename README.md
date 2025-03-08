# QuickRail Chatbot

## Project Description
QuickRail is an interactive train ticket booking system built using Streamlit. It allows users to book train tickets for different routes across India. The chatbot takes users through the booking process step-by-step, from selecting departure and destination stations to class preferences and payment. This app also provides real-time information about stations, train statuses, PNR status, and fare details.

### Key Features:
- **Train Ticket Booking**: Users can select their departure and destination stations, choose the class (Sleeper/AC), and proceed to make payments.
- **Real-Time Information**: The app fetches live data on station details, train statuses, and PNR status using the IRCTC API.
- **Payment Integration**: The system supports mock payment processing, where users can select their preferred payment method.
- **Lottie Animations**: Beautiful animations enhance the user experience during the booking process.

## Tech Stack
- **Frontend**: Streamlit, HTML, CSS, Lottie animations
- **Backend**: Python
- **APIs Used**: 
  - IRCTC API for station details, live train status, and fare info
  - RapidAPI for real-time information (train status, PNR status)

## Features
### Step-by-Step Booking Process:
1. Choose number of passengers.
2. Select departure and destination stations.
3. Choose the class (Sleeper/AC).
4. Calculate fare and confirm payment.

### Real-Time Information:
- Check station details by station code.
- Check the live status of any train.
- Get PNR status and track booking progress.
- Fetch train fare details based on class and quota.

## Installation
To run this project locally, follow these steps:

1. **Clone the repository**:

    ```bash
    git clone https://github.com/jasmeettt/Chatbot.git
    cd Chatbot
    ```

2. **Install the dependencies**: Make sure you have pip installed, and then run:

    ```bash
    pip install -r requirements.txt
    ```

   You may need to create a `requirements.txt` file that lists the following dependencies:

    ```txt
    streamlit
    streamlit-option-menu
    streamlit-lottie
    requests
    ```

3. **Run the app**: After installing the dependencies, run the app using the command:

    ```bash
    streamlit run app.py
    ```

4. Open a web browser and visit `http://localhost:8501` to access the chatbot.

## Usage
### Start Booking Process:
When you click "🎟️ Book your Tickets Now," the bot will ask you a series of questions:
1. Number of passengers
2. Departure station
3. Destination station
4. Choose the class (Sleeper/AC)
5. Calculate the fare for your trip
6. Proceed to payment

### Live Train Information:
You can also use the sidebar to access real-time station, train, and PNR status by selecting the respective options.

### Payment Portal:
When you're ready to confirm your booking, proceed to the payment section. Here, you can choose a payment method (Credit/Debit Card, UPI, Wallet, etc.).

### Thank You Page:
After confirming payment, the chatbot will show a success message and display a thank-you animation.

## Lottie Animations
This project uses Lottie animations to provide a more engaging user experience. The animations are loaded via the `st_lottie` Streamlit component. You can find the JSON files for these animations in the `assets/` directory.

## Contributing
If you have any suggestions, improvements, or bugs to report, feel free to fork the repository and submit a pull request. Contributions are always welcome!

## License
This project is licensed under the MIT License - see the LICENSE file for details.

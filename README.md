# 🚆 QuickRail Chatbot  

## **Project Description**  
QuickRail is an interactive **train ticket booking system** built using **Streamlit**. It allows users to book train tickets for different routes across India. The chatbot takes users through the **step-by-step booking process**, from selecting departure and destination stations to class preferences and payment. The app also provides **real-time train-related information** such as station details, train statuses, PNR status, and fare details by fetching data from a **Flask API with a dataset**.  

### **Key Features**  
- **Train Ticket Booking**: Users can select their departure and destination stations, choose the class (Sleeper/AC), and proceed to make payments.  
- **Real-Time Information**: The app fetches train-related data (station details, train status, PNR status, fare info) from a **Flask API** instead of external sources.  
- **Payment Integration**: Supports mock payment processing, allowing users to select their preferred payment method.  
- **Lottie Animations**: Beautiful animations enhance the user experience during the booking process.  

---

## **Tech Stack**  
- **Frontend**: Streamlit, HTML, CSS, Lottie animations  
- **Backend**: Python (Flask)  
- **APIs Used**:  
  - **Custom Flask API** for train details, station status, and fare information  

---

## **Features**  

### **Step-by-Step Booking Process**  
1. Choose the number of passengers.  
2. Select **departure** and **destination** stations.  
3. Choose a **class** (Sleeper/AC).  
4. Calculate **fare** and confirm **payment**.  

### **Real-Time Information**  
- Check **station details** by station code.  
- Check the **live status** of any train.  
- Get **PNR status** and track booking progress.  
- Fetch **train fare details** based on class and quota.  

---

## **Installation**  

To run this project locally, follow these steps:  

1. **Clone the repository**  
    ```bash
    git clone https://github.com/jasmeettt/Chatbot.git
    cd Chatbot
    ```

2. **Install dependencies**  
    ```bash
    pip install streamlit streamlit-option-menu streamlit-lottie requests flask pandas
    ```

3. **Run the Flask API**  
    ```bash
    python api.py
    ```
    ✅ Flask API runs on `http://127.0.0.1:5001`.  

4. **Run the Streamlit app**  
    ```bash
    streamlit run app.py
    ```

5. Open a web browser and visit **`http://localhost:8501`** to access the chatbot.  

---

## **Usage**  

### **🎟️ Start Booking Process**  
When you click **"🎟️ Book your Tickets Now,"** the chatbot will guide you through:  
✔ Number of passengers  
✔ Departure station  
✔ Destination station  
✔ Choose class (**Sleeper/AC**)  
✔ Calculate **fare**  
✔ Proceed to **payment**  

### **📡 Live Train Information**  
You can also use the **sidebar** to access:  
- **Station details**  
- **Live train status**  
- **PNR status tracking**  
- **Train fare details**  

### **💳 Payment Portal**  
Confirm your booking and choose a **payment method** (**Credit/Debit Card, UPI, Wallet, etc.**).  

### **🎉 Thank You Page**  
After payment, a **confirmation message & Lottie animation** will be displayed.  

---

## **🎨 Lottie Animations**  
This project uses **Lottie animations** to enhance the user experience. The animations are loaded via the `st_lottie` Streamlit component. JSON files are located in the `assets/` directory.  

---

## **🔗 Inspiration**  
This project was inspired by [Deekshith B](https://www.youtube.com/channel/UCg0r6zCTkX5R5ikU9T-PwDg), whose YouTube tutorial on a train booking chatbot provided the foundation. I improved the project by **developing a Flask API** instead of using external APIs.  

---

## **🤝 Contributing**  
If you have any **suggestions, improvements, or bug reports**, feel free to **fork the repository** and submit a **pull request**. Contributions are always welcome! 🚀  

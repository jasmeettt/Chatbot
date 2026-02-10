# 🚆 QuickRail Chatbot

An interactive **train ticket booking and information system** built with **Streamlit** and powered by a **Flask API**. QuickRail guides users through ticket booking, provides train status, PNR lookups, station info, and fare details — all through a conversational chatbot interface.

---

## ✨ Features

### 🎟️ Train Ticket Booking
- Step-by-step guided booking via chatbot
- Choose number of passengers, train, and class (SL / 3A / 2A / 1A)
- Mock payment with multiple methods (Card, UPI, Net Banking, Wallet)
- **Downloadable PDF ticket** after successful payment

### 🤖 General Chatbot
- Ask about train status, PNR, station info, or fares using natural language
- Input validation (e.g., PNR must be 10 digits)
- Helpful fallback messages for unrecognized queries

### 📍 Train Services Dashboard
- **Station Details** — Look up any station by code
- **Train Live Status** — Check if a train is on time or delayed
- **PNR Status** — Get booking confirmation and seat details
- **Train Fare** — Compare fares across classes and quotas

### 🎨 UI Enhancements
- Lottie animations for booking and payment success
- Loading spinners on all API-dependent actions
- Clean sidebar navigation

---

## 🛠️ Tech Stack

| Layer | Technology |
|:------|:-----------|
| Frontend | Streamlit, Lottie Animations |
| Backend API | Python Flask |
| PDF Generation | FPDF |
| Data | In-memory dictionaries (no database needed) |

---

## 🚀 How to Run

### Prerequisites
- **Python 3.10+** installed
- **pip** available in your PATH

### Step 1: Clone the Repository
```bash
git clone https://github.com/jasmeettt/Chatbot.git
cd Chatbot
```

### Step 2: Create a Virtual Environment
```bash
python -m venv venv
```

### Step 3: Activate the Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\activate
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Start the Flask API (Terminal 1)
```bash
python api.py
```
> The API will start on `http://127.0.0.1:5001`

### Step 6: Start the Streamlit App (Terminal 2)
```bash
streamlit run home_page.py
```
> The app will open at `http://localhost:8501`

---

## 📁 Project Structure

```
Chatbot/
├── api.py                  # Flask API with train, station, PNR & fare data
├── home_page.py            # Streamlit UI — main entry point
├── rule_based_chatbot.py   # Chatbot logic, booking flow, PDF generation
├── requirements.txt        # Python dependencies
├── .gitignore              # Excludes venv, cache, generated files
├── assets/
│   ├── quic_rail.json      # Lottie animation for booking page
│   ├── payment_success.json# Lottie animation for payment confirmation
│   └── *.webp              # Banner image for home page
└── README.md
```

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|:---------|:-------|:------------|
| `/` | GET | Welcome message |
| `/station/<code>` | GET | Get station details by code (e.g., NDLS, CSMT) |
| `/train_status/<number>` | GET | Get live status of a train |
| `/pnr_status/<pnr>` | GET | Get PNR booking status |
| `/train_fare?train_number=&class=` | GET | Get fare for a train and class |

---

## 🧪 Sample Data

The API uses in-memory data. Here are some values you can test with:

| Type | Sample Values |
|:-----|:-------------|
| **Station Codes** | NDLS, CSMT, MMCT, PUNE, SBC, MAS, TNA, KYN, PNVL |
| **Train Numbers** | 12431, 11027, 12625, 12951, 22120 |
| **PNR Numbers** | 1234567890, 9876543210, 5678901234 |

---

## 🤝 Contributing

Suggestions, improvements, and bug reports are welcome!  
Fork the repo, make your changes, and submit a pull request. 🚀

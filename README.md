# 🥗 MacroSnap — AI Vision Nutrition Chatbot

MacroSnap is a Streamlit chat application where users enter their name and WhatsApp number, chat with an AI nutrition buddy (by typing questions or uploading food photos), get instant calorie/macro estimates, and send a complete nutrition summary straight to WhatsApp via Twilio.

---

## 📁 Project Structure

```
AI_Vision_Nutrition_bot/
├── app.py                        # Main Streamlit application logic
├── prompts.py                    # AI System Prompts & message templates
├── requirements.txt              # Project dependencies
├── .gitignore                    # Prevents secret credentials & venv from being committed
└── .streamlit/
    └── secrets.toml.example      # Template for Streamlit secrets configuration
```

---

## ⚡ Prerequisites & Setup

### 1. Requirements
- Python 3.9+
- Google Gemini API Key ([Google AI Studio](https://aistudio.google.com/))
- Twilio Account SID, Auth Token & WhatsApp Content SID ([Twilio Console](https://www.twilio.com/console))

### 2. Local Installation

1. **Clone or Extract the Project:**
   ```bash
   cd AI_Vision_Nutrition_bot
   ```

2. **Create & Activate Virtual Environment:**
   - **Windows PowerShell:**
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Secrets:**
   Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and fill in your API credentials:
   ```toml
   GEMINI_API_KEY = "your-gemini-api-key"
   TWILIO_ACCOUNT_SID = "your-twilio-account-sid"
   TWILIO_AUTH_TOKEN = "your-twilio-auth-token"
   TWILIO_WHATSAPP_FROM = "whatsapp:+14155238886"
   TWILIO_CONTENT_SID = "your-content-template-sid"
   ```

---

## 🚀 Running the App

Run the Streamlit server locally:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🌐 Deploying to Streamlit Community Cloud

1. Push your repository to GitHub (ensure `.streamlit/secrets.toml` is **not** committed).
2. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with GitHub.
3. Click **New app**, select your repository, branch, and set `app.py` as the entry point.
4. Under **Settings → Secrets**, paste the keys from your `secrets.toml`.
5. Deploy!

# Restaurant Intelligence MVP

This is a lightweight Streamlit-based MVP for small restaurant owners to forecast inventory, compare vendors, view local event impact, and interact with an AI assistant for smart decision-making.

## 📦 Features
- Inventory usage visualization with seasonality and spikes
- 7-day inventory forecast (simulated for now)
- Vendor suggestions ranked by price and reliability
- Event-based demand insights
- OpenAI-powered assistant chatbot

## 🚀 How to Run Locally
```bash
git clone https://github.com/KHADIJAARSLAN/restaurant-intelligence-mvp.git
cd restaurant-intelligence-mvp
pip install -r requirements.txt
streamlit run app.py
```

## 📁 Project Structure
```
restaurant-intelligence-mvp/
├── app.py
├── inventory_with_seasonality.csv
├── vendors.csv
├── events.csv
├── requirements.txt
├── .streamlit/
│   └── secrets.toml  ← (Not included; create yourself)
└── README.md
```

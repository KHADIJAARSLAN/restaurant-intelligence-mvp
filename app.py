import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from openai import OpenAI, RateLimitError

# Page setup
st.set_page_config(page_title="Restaurant Intelligence Platform", layout="wide")
st.title("🍽️ Restaurant Intelligence Dashboard")

# Load data
inventory_df = pd.read_csv("inventory_with_seasonality.csv")
vendor_df = pd.read_csv("vendors.csv")
event_df = pd.read_csv("events.csv")

# Sidebar selection
item = st.sidebar.selectbox("Select an Ingredient", inventory_df["Item"].unique())

# Filter inventory data
filtered_inventory = inventory_df[inventory_df["Item"] == item]
filtered_inventory = filtered_inventory.sort_values("Date")

# Plot usage
st.subheader(f"📊 Usage Trend for {item.title()}")
# Plot with better x-axis formatting
fig, ax = plt.subplots()
ax.plot(pd.to_datetime(filtered_inventory['Date']), filtered_inventory['Used_kg'])
ax.set_xlabel('Date')
ax.set_ylabel('Used (kg)')
fig.autofmt_xdate()
st.pyplot(fig)

# Forecast (Simulated for now)
st.subheader("🔮 7-Day Forecast")
last_mean = filtered_inventory.tail(14)["Used_kg"].mean()
forecast = pd.DataFrame({
    "Date": pd.date_range(start=filtered_inventory["Date"].iloc[-1], periods=8, freq='D')[1:],
    "Forecast_kg": [round(last_mean * 1.1, 2)] * 7
})
st.dataframe(forecast)

# Vendor Suggestions
st.subheader(f"💡 Vendor Suggestions for {item.title()}")
vendor_options = vendor_df[vendor_df["Item"] == item].sort_values("Price_per_kg")
st.dataframe(vendor_options)

# Event Alerts
st.subheader("📅 Upcoming Events in Berkeley")

# Debug view to inspect raw event data
st.write("All events loaded:")
st.dataframe(event_df)

# Ensure dates are parsed correctly
event_df["Date"] = pd.to_datetime(event_df["Date"], errors='coerce')
today = pd.Timestamp.today()

upcoming_events = event_df[event_df["Date"] > today].sort_values("Date")

st.write("Filtered upcoming events:")
st.dataframe(upcoming_events)

if not upcoming_events.empty:
    for _, row in upcoming_events.head(10).iterrows():
    event_name = row['Event_Name']
    if 'Berkeley Event 1' in event_name:
        event_name = 'Berkeley Graduation Day'
    elif 'Berkeley Event 2' in event_name:
        event_name = 'Downtown Food Festival'
    elif 'Berkeley Event 3' in event_name:
        event_name = 'Cal Football Game Day'
    st.markdown(f"**{event_name}** — {row['Date'].date()} *(Impact: {row['Impact_Level']})*")
else:
    st.info("No upcoming events found after today's date.")

# Chatbot Section
st.subheader("💬 Ask the Assistant")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

query = st.text_input("Ask a question about your inventory, vendors, or forecasts:")
if query:
    with st.spinner("Thinking..."):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You're a helpful restaurant data assistant."},
                    {"role": "user", "content": query}
                ]
            )
            st.success(response.choices[0].message.content)
        except RateLimitError:
            st.error("⚠️ Rate limit reached. Please try again later or check your OpenAI usage.")
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {e}")




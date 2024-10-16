import streamlit as st
import pandas as pd
import gspread
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)


# Constants: Public Google Sheet link and worksheet setup
SHEET_URL = "https://docs.google.com/spreadsheets/d/12JIjGKy0TUTHO8HmnSc88JhtutxONOblF94Q5D41KRs"
gc = gspread.service_account()  # Requires Google Sheets API service account JSON in your project directory
worksheet = gc.open_by_url(SHEET_URL).sheet1  # Access the first worksheet

# Helper function to determine Sunday event window
def get_event_window():
    today = datetime.now()
    last_sunday = today - timedelta(days=today.weekday() + 1) if today.weekday() != 6 else today
    next_sunday = last_sunday + timedelta(days=7)
    return last_sunday, next_sunday

last_sunday, next_sunday = get_event_window()

# Load RSVP data from the Google Sheet into a DataFrame
data = worksheet.get_all_records()
df = pd.DataFrame(data)

st.title("RSVP to Sunday Event")

# RSVP Submission Form
with st.form("RSVP Form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    attending = st.selectbox("Will you attend?", ["Yes", "No", "Maybe"])
    submit = st.form_submit_button("Submit")

    if submit:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        worksheet.append_row([name, email, attending, timestamp])
        st.success(f"Thank you, {name}! Your RSVP has been recorded.")

# Display upcoming event details and RSVPs
st.header("RSVP List for Upcoming Event")

# Filter RSVPs for the upcoming Sunday event
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format="%Y-%m-%d %H:%M:%S")
upcoming_rsvps = df[(df['Timestamp'] >= last_sunday) & (df['Timestamp'] < next_sunday)]

if not upcoming_rsvps.empty:
    st.dataframe(upcoming_rsvps[['Name', 'Email', 'Attendance Status']])
else:
    st.write("No RSVPs yet for the upcoming event.")

# Display last Sunday and upcoming Sunday for debugging purposes
st.sidebar.write(f"Last Sunday: {last_sunday.strftime('%Y-%m-%d')}")
st.sidebar.write(f"Upcoming Sunday: {next_sunday.strftime('%Y-%m-%d')}")

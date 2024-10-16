import streamlit as st
import gspread
import pandas as pd

# Connect to the Google Sheet (replace 'your-sheet-id' with the actual ID)
SHEET_ID = "your-google-sheet-id"
gc = gspread.service_account()  # Ensure service account JSON is in your project folder
sh = gc.open_by_url(https://docs.google.com/spreadsheets/d/12JIjGKy0TUTHO8HmnSc88JhtutxONOblF94Q5D41KRs/edit?usp=sharing)
worksheet = sh.get_worksheet(0)  # Access the first sheet

# Load data into a pandas DataFrame
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# Streamlit App Logic
st.title("RSVP to Event")

# RSVP Form
with st.form("rsvp_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    attending = st.selectbox("Will you attend?", ["Yes", "No", "Maybe"])
    submit = st.form_submit_button("Submit")

    if submit:
        # Append new row to Google Sheet
        worksheet.append_row([name, email, attending, pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")])
        st.success("Thank you for your RSVP!")

# Display current RSVP list
st.header("RSVP List")
st.dataframe(df)

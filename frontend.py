import streamlit as st
import requests

# Fetch market data from Flask backend
response = requests.get('http://localhost:5000/api/market_data')
market_data = response.json()

# Display market data
for key, df in market_data.items():
    st.write(f"### {key}")
    st.write(df)

# Allow user to select a market for prediction
selected_market = st.selectbox('Select a market for prediction', list(market_data.keys()))

# Allow user to input future data
future_date = st.date_input('Enter future date')
future_close_price = st.number_input('Enter future close price')

# Send data to Flask backend for prediction
if st.button('Predict'):
    data = {
        'market_data': market_data,
        'selected_market': selected_market,
        'future_data': {
            'Date': future_date.strftime('%Y-%m-%d'),
            'Close': future_close_price
        }
    }
    response = requests.post('http://localhost:5000/api/predict', json=data)
    prediction = response.json()['prediction']
    st.write(f"Predicted close price: {prediction}")

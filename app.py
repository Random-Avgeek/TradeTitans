from flask import Flask, jsonify, request
import pandas as pd
import sklearn
from sklearn.linear_model import LinearRegression
import csv

app = Flask(__name__)

@app.route('/api/market_data', methods=['GET'])
def get_market_data():
    dataframes = {"market_data_1.csv","market_data_2.csv","market_data_3.csv", "market_data_4.csv", "market_data_5.csv", "market_data_6.csv", "market_data_7.csv", "market_data_8.csv", "market_data_9.csv", "market_data_10.csv"}
    for i in range(1, 11):
        with open(f'market_data_{i}.csv', 'r') as file:
            reader = csv.reader(file)
            data = [row for row in reader]
            dataframes[f'market_data_{i}'] = pd.DataFrame(data[1:], columns=data[0])

    return jsonify(dataframes)

@app.route('/api/predict', methods=['POST'])
def predict():
    # Get data from request
    data = request.json
    market_data = data['market_data']
    selected_market = data['selected_market']
    future_data = data['future_data']

    # Load the selected market data
    with open(f'{selected_market}.csv', 'r') as file:
        reader = csv.reader(file)
        df = pd.DataFrame([row for row in reader])

    # Train a simple Linear Regression model (you can use a more advanced model)
    X = df.iloc[1:, [0, 4]]  # Assuming Date is in the first column and Close is in the fifth column
    y = df.iloc[1:, 4]
    model = LinearRegression()
    model.fit(X, y)

    # Predict future data
    future_prediction = model.predict([[future_data['Date'], future_data['Close']]])

    # Return prediction
    return jsonify({'prediction': future_prediction[0]}) 

if __name__ == '__main__':
    app.run(debug=True)

#!/usr/bin/env python
# coding: utf-8

# # Car Price Prediction using Machine Learning

# In[31]:


# Importing the dependencies
import sys
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5 import QtGui


# In[32]:


# Loading the dataset 
data = pd.read_csv('quikr_car.csv')

# Cleaning the dataset by replacing '...' with NaN and dropping rows with missing values
data = data.replace('...', np.nan)
data = data.dropna()


# In[ ]:


# Converting 'year' and 'kms_driven' columns to strings
data['year'] = data['year'].astype(str)
data['kms_driven'] = data['kms_driven'].str.replace(' kms', '').str.replace(',', '')

# Filtering out rows with invalid 'year' and 'kms_driven' values
data = data[data['year'].str.isnumeric()]
data = data[data['kms_driven'].str.isnumeric()]

# Converting 'Price' column to float (remove ' Lakh' and ',')
y = data['Price'].str.replace(' Lakh', '').str.replace(',', '').astype(float)

# Performing one-hot encoding for the 'fuel_type' column
data = pd.get_dummies(data, columns=['fuel_type'], drop_first=True)

# Features and target variable
X = data[['year', 'kms_driven', 'fuel_type_Petrol']]  

# Convert numeric columns to the correct data type (int or float)
X['year'] = X['year'].astype(int)
X['kms_driven'] = X['kms_driven'].str.replace(',', '').astype(int)


# In[ ]:


# Create and train a Linear Regression model
model = LinearRegression()
model.fit(X, y)


# In[36]:


# Main function
class CarPricePredictorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Car Price Prediction')
        self.setGeometry(200, 200, 500, 400)  # Increased the height

        layout = QVBoxLayout()

        title_label = QLabel('<h1 style="font-family:Poppins; font-weight: bold; font-size: 24px;">Car Price Prediction</h1>')
        layout.addWidget(title_label)

        self.name_label = QLabel('<span style="font-family: Arial; font-weight: bold; font-size: 16px;">Car Model:</span>')
        self.year_label = QLabel('<span style="font-family: Arial; font-weight: bold; font-size: 16px;">Year:</span>')
        self.kms_label = QLabel('<span style="font-family: Arial; font-weight: bold; font-size: 16px;">Kilometers Driven:</span>')
        self.fuel_label = QLabel('<span style="font-family: Arial; font-weight: bold; font-size: 16px;">Fuel Type (Petrol):</span>')

        self.name_input = QLineEdit()
        self.year_input = QLineEdit()
        self.kms_input = QLineEdit()
        self.fuel_input = QLineEdit()
        
        self.name_input.setFont(QtGui.QFont("Arial", 12))  
        self.year_input.setFont(QtGui.QFont("Arial", 12))  
        self.kms_input.setFont(QtGui.QFont("Arial", 12))  
        self.fuel_input.setFont(QtGui.QFont("Arial", 12))

        self.predict_button = QPushButton('Predict Price')
        self.predict_button.setStyleSheet("background-color: green; color: white; font-family: Poppins; font-weight: bold; font-size: 18px; padding: 5px 5px;")

        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.year_label)
        layout.addWidget(self.year_input)
        layout.addWidget(self.kms_label)
        layout.addWidget(self.kms_input)
        layout.addWidget(self.fuel_label)
        layout.addWidget(self.fuel_input)
        layout.addWidget(self.predict_button)

        self.result_label = QLabel('<h2 style="font-family: Poppins; font-weight: bold; font-size: 20px; color: blue;">Predicted Price:</h2>')
        layout.addWidget(self.result_label)

        self.setLayout(layout)

        self.predict_button.clicked.connect(self.predict_price)

    def predict_price(self):
        try:
            name = self.name_input.text()
            year = int(self.year_input.text())
            kms_driven = int(self.kms_input.text())
            fuel_type_petrol = 1  # Set to 1 for 'Petrol,' as it's one-hot encoded

            # Create an input DataFrame for prediction
            input_data = pd.DataFrame({
                'year': [year],
                'kms_driven': [kms_driven],
                'fuel_type_Petrol': [fuel_type_petrol]
            })

            # Predict price
            predicted_price = model.predict(input_data)

            self.result_label.setText(f'<h2 style="font-family: Poppins; font-weight: bold; font-size: 18px; color: blue;">Predicted Price: Rs. {predicted_price[0]:.2f}</h2>')

        except Exception as e:
            QMessageBox.warning(self, 'Error', 'Please enter valid input.')

def main():
    app = QApplication(sys.argv)
    window = CarPricePredictorApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


# In[ ]:





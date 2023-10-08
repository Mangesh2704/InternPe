#!/usr/bin/env python
# coding: utf-8

# # Breast Cancer Prediction using Machine Learning

# In[ ]:


#Importing the dependencies
import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split

# Loading the breast cancer dataset
data = pd.read_csv('data.csv')

# Preprocessing the dataset
label_encoder = LabelEncoder()
data['diagnosis'] = label_encoder.fit_transform(data['diagnosis'])

imputer = SimpleImputer(strategy='mean')
data = imputer.fit_transform(data) 

X = data[:, 2:7]  
y = data[:, 1]  

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)


#Main Function

class BreastCancerDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Breast Cancer Detection")
        self.setGeometry(100, 100, 600, 400)  
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
 
        title_label = QLabel("Breast Cancer Detection")
        title_label.setAlignment(Qt.AlignLeft)
        title_font = QFont("Arial", 18, QFont.Bold)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        parameter_labels = [
            "Radius Mean:",
            "Texture Mean:",
            "Perimeter Mean:",
            "Area Mean:",
            "Smoothness Mean:"
        ]
        
        self.input_fields = []
        
        for label_text in parameter_labels:
            label = QLabel(label_text)
            label.setFont(QFont("Arial", 12, QFont.Bold))  
            layout.addWidget(label)
            input_field = QLineEdit()
            layout.addWidget(input_field)
            input_field.setFont(QFont("Arial", 12)) 
            self.input_fields.append(input_field)
  
        detect_button = QPushButton("Detect Cancer")
        detect_button.clicked.connect(self.detect_cancer)
        detect_button.setStyleSheet("background-color: #4CAF50; color: white;")
        layout.addWidget(detect_button)
        
        self.result_label = QLabel("")
        result_font = QFont("Arial", 14, QFont.Bold)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(result_font)
        layout.addWidget(self.result_label)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    
    def detect_cancer(self):

        input_values = [float(field.text()) for field in self.input_fields]

        input_data = pd.DataFrame([input_values]).values

        prediction = clf.predict(input_data)

        if prediction[0] == 1:
            self.result_label.setText("Malignant (Cancerous)")
            self.result_label.setStyleSheet("color: red;")
        else:
            self.result_label.setText("Benign (Not Cancerous)")
            self.result_label.setStyleSheet("color: green;")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BreastCancerDetectionApp()
    window.show()
    sys.exit(app.exec_())


# In[ ]:





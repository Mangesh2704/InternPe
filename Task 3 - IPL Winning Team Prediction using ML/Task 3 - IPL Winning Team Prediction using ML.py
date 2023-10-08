#!/usr/bin/env python
# coding: utf-8

# # IPL Winning Team Prediction using Machine Learning

# In[1]:


# Importing the dependencies
import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor


# In[2]:


# Loading the 'matches.csv' dataset
matches = pd.read_csv('matches.csv')

# Loading the 'teams.csv' dataset
teams = pd.read_csv('teams.csv')


# In[ ]:


# Main Function

class IPLPredictionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IPL Team Prediction")
        self.setGeometry(100, 100, 600, 300)  
        
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        title_label = QLabel("IPL Winning Team Prediction")
        title_label.setAlignment(Qt.AlignLeft)
        title_font = QFont("Poppins", 16)  
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        select_team1_label = QLabel("Select Team 1:")
        select_team2_label = QLabel("Select Team 2:")
        select_venue_label = QLabel("Select Venue:")
        select_toss_winner_label = QLabel("Select Toss Winner:")

        select_labels = [select_team1_label, select_team2_label, select_venue_label, select_toss_winner_label]
        for label in select_labels:
            label.setFont(QFont("Arial", 12, QFont.Bold)) 
            
        self.team1_combobox = QComboBox()
        self.team1_combobox.addItems(teams['team1'].unique())
        
        self.team2_combobox = QComboBox()
        self.team2_combobox.addItems(teams['team1'].unique())
        
        self.venue_combobox = QComboBox()
        self.venue_combobox.addItems(matches['venue'].unique())
        
        self.toss_winner_combobox = QComboBox()
        self.toss_winner_combobox.addItems(matches['toss_winner'].unique())
        
        predict_button = QPushButton("Predict Winner")
        predict_button.clicked.connect(self.predict_winner)
        
        button_font = QFont("Poppins", 14)
        button_font.setBold(True)
        predict_button.setFont(button_font)

        predict_button.setStyleSheet("background-color: #4CAF50; color: white; border: none; padding: 10px;")
        
        self.result_label = QLabel()
        result_font = QFont("Poppins", 14)  
        result_font.setBold(True)
        self.result_label.setFont(result_font)
        
        layout.addWidget(select_team1_label)
        layout.addWidget(self.team1_combobox)
        layout.addWidget(select_team2_label)
        layout.addWidget(self.team2_combobox)
        layout.addWidget(select_venue_label)
        layout.addWidget(self.venue_combobox)
        layout.addWidget(select_toss_winner_label)
        layout.addWidget(self.toss_winner_combobox)
        layout.addWidget(predict_button)
        layout.addWidget(self.result_label)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    
    def predict_winner(self):
        team1 = self.team1_combobox.currentText()
        team2 = self.team2_combobox.currentText()
        venue = self.venue_combobox.currentText()
        toss_winner = self.toss_winner_combobox.currentText()
        
        selected_match = matches[(matches['team1'] == team1) & (matches['team2'] == team2) &
                                 (matches['venue'] == venue) & (matches['toss_winner'] == toss_winner)]
        
        if not selected_match.empty:
            team1_wins = selected_match[selected_match['winner'] == team1].shape[0]
            team2_wins = selected_match[selected_match['winner'] == team2].shape[0]
            
            if team1_wins > team2_wins:
                winning_team = team1
            elif team2_wins > team1_wins:
                winning_team = team2
            else:
                winning_team = "It's a tie"
                blue_color = QColor(0, 0, 255)
                palette = QPalette()
                palette.setColor(QPalette.WindowText, blue_color)
                self.result_label.setPalette(palette)
            
            self.result_label.setText(f'Predicted Winning Team: {winning_team}')
        else:
            blue_color = QColor(0, 0, 255)
            palette = QPalette()
            palette.setColor(QPalette.WindowText, blue_color)
            self.result_label.setPalette(palette)
            
            self.result_label.setText('No match found for the selected parameters.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = IPLPredictionApp()
    window.show()
    sys.exit(app.exec_())


# In[ ]:





# In[ ]:





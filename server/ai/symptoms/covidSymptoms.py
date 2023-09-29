import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.neural_network import MLPClassifier
from sklearn import metrics
import pickle

class NeuralNetwork:
    def __init__(self, relevant_features):
        self.model = self.load_model()
        self.relevant_features = relevant_features

    def load_model(self, filename='nn_model.pkl'):
        with open(filename, 'rb') as model_file:
            return pickle.load(model_file)

    def predict(self, X):
        relevant_X = X[self.relevant_features]
        return self.model.predict(relevant_X)

    def predict_proba(self, X):
        relevant_X = X[self.relevant_features]
        return self.model.predict_proba(relevant_X)

covid = pd.read_csv('./symptom_data/Covid_Dataset.csv')

relevant_features = ['Breathing Problem', 'Fever', 'Dry Cough', 'Sore throat', 'Abroad travel',
                     'Contact with COVID Patient', 'Visited Public Exposed Places', 'Wearing Masks',
                     'Sanitization from Market', 'Fatigue ']

for col in relevant_features:
    e = LabelEncoder()
    covid[col] = e.fit_transform(covid[col])

covid['COVID-19'] = covid['COVID-19'].map({'No': 0, 'Yes': 1})

x = covid.drop('COVID-19', axis=1)
y = covid['COVID-19']


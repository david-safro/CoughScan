import pandas as pd
from sklearn.model_selection import train_test_split


def load_and_preprocess_data(file_path='covid.csv'):
    covid_data = pd.read_csv(file_path)

    new_column_names = {
        'Breathing Problem': 'breathing',
        'Fever': 'fever',
        'Dry Cough': 'dry-cough',
        'Sore throat': 'sore-throat',
        'Running Nose': 'running-nose',
        'Asthma': 'asthma',
        'Chronic Lung Disease': 'chronic-lung',
        'Headache': 'headache',
        'Heart Disease': 'heart-disease',
        'Diabetes': 'diabetes',
        'Fatigue ': 'fatigue',
        'Gastrointestinal ': 'gastrointestinal',
        'Abroad travel': 'abroad-travel',
        'Contact with COVID Patient': 'contact-covid',
        'Attended Large Gathering': 'large-gathering',
        'Visited Public Exposed Places': 'public-places',
        'Family working in Public Exposed Places': 'family-public',
        'Wearing Masks': 'masks',
        'Sanitization from Market': 'sanitization',
        'COVID-19': 'covid-19'
    }
    covid_data = covid_data.rename(columns=new_column_names)

    covid_data = covid_data.replace({'Yes': 1, 'No': 0})

    y = covid_data['covid-19']
    X = covid_data.drop('covid-19', axis=1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    X_train = X_train.fillna(0)
    X_test = X_test.fillna(0)

    return X_train, X_test, y_train, y_test

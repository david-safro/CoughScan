import pickle
from feature import make_nonsemantic_frill_nofrontend_feat

def predict(audio_file, model_filename='covid_model_fold0.pkl'):
    with open(model_filename, 'rb') as file:
        model = pickle.load(file)
    features = make_nonsemantic_frill_nofrontend_feat(audio_file)
    features = features.reshape(1, -1)
    prediction = model.predict(features)

    probability = model.predict_proba(features)[0][prediction[0]]

    return prediction[0], probability


audio_file = 'audiocough.wav'
model_filename = './sounddr_data/output/covid_model_fold0.pkl'
prediction = predict(audio_file, model_filename)
print(f'Prediction: {prediction}')

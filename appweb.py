from flask import Flask, request, redirect, url_for, send_file,render_template,flash
from werkzeug.utils import secure_filename
import os
import numpy as np
from keras.models import load_model


# Charge le modèle lors du démarrage de l'application Flask
model = load_model('model.h5')



app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route pour la page d'accueil
@app.route('/')
def home():
    return render_template('index.html')

# Route pour la soumission du formulaire
@app.route('/predict', methods=['POST'])
def predict():
    if 'video_file' not in request.files:
        return "Aucun fichier trouvé !"
    
    file = request.files['video_file']
    
    if file.filename == '':
        return "Nom de fichier vide !"

    # Sauvegarder le fichier vidéo dans le répertoire d'uploads
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(video_path)

    # Appeler ton modèle de prédiction pour obtenir la prédiction
    prediction = model.predict(video_path)  
    
    # Retourner les résultats à afficher sur la page de résultats
    return render_template('results.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
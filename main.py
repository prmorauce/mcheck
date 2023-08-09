#Importo las librerías 
import cv2
import pandas as pd
from deepface import DeepFace
from flask import Flask, request, jsonify
import os

#Defino el nombre de la App
app = Flask(__name__)

#Defino la carpeta donde subir la imagen y algunas configuraciones
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
#Defino las extensiones de imagenes permitidas
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

#Función para validar extensión del archivo
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

#Firma principla de la Api
@app.route('/getDominantEmotion', methods=['GET', 'POST'])
def getDominantEmotion():
    if request.method == "GET":
        #Defino modelo de datos
        data = {"Emotions": [], "DominantEmotion": [],}
        #Analizo la imagen con librería DeepFace y obtengo solo la caracteristica de Emociones
        result = DeepFace.analyze(cv2.imread("faces/3.png"), actions=("emotion"))
        data["Emotions"].append(result[0]["emotion"])
        data["DominantEmotion"].append(result[0]["dominant_emotion"])
        #Genero un cuadro con la data
        df = pd.DataFrame(data)
        #Imprimo Data
        print(df)
        #Genero JSON 
        return jsonify(data)
    
    elif request.method == "POST":
        #Valido que se envíe el parametro con la imagen
        if 'file' not in request.files:
            resp = jsonify({'message': 'No file part in the request', 'status': 400})
            resp.status_code = 400
            return resp
        
        files = request.files.getlist('file')
        errors = {}
        success = False

        #Barro la imagen seleccionada
        for file in files:
            #Valido que la imagen cumpla con las caracteristicas establecidas
            if file and allowed_file(file.filename):
                #subo archivo en carpeta designada y coloco un nombre 
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'image.jpg'))
                success = True
            else:
                errors['error'] = 'File type is not allowed'
        
        if success:
            #Defino modelo de datos
            data = {"Emotions": [], "DominantEmotion": [],}
            #Analizo la imagen con librería DeepFace y obtengo solo la caracteristica de Emociones
            result = DeepFace.analyze(cv2.imread("uploads/image.jpg"), actions=("emotion"), enforce_detection=False)
            data["Emotions"].append(result[0]['emotion'])
            data["DominantEmotion"].append(result[0]['dominant_emotion'])
            #Genero la respuesta en JSON
            resp = jsonify({'message': 'File successfully upload', 'status': 200, 'data': data})
            resp.status_code = 200
            return resp
        else:
            resp = jsonify({'message': errors, 'status': 500})
            resp.status_code = 500
            return resp

if __name__ == '__main__':
    app.run(debug=True, port=5000)

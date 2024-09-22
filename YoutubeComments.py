from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import requests
import time

load_dotenv()

#Clave para APIs de Google Cloud
api_key = 'AIzaSyA5Wm4XH80ajTTEHRe57rOYU-XVo1sQK9I'
api_token = "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" # get yours at hf.co/settings/tokens


def query(payload, model_id, api_token):
	headers = {"Authorization": f"Bearer {api_token}"}
	API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

model_id = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"



# URL base de la API de YouTube
youtube = build('youtube', 'v3', developerKey=api_key)
def obtener_comentarios_recientes(video_id, max_results=8):
    comentarios = []
    respuesta = youtube.commentThreads().list(
        part = 'snippet',
        videoId = video_id,
        textFormat= 'plainText',
        maxResults = max_results,
        order='time'
    ).execute()
    for item in respuesta['items']:
       comentario = item['snippet']['topLevelComment']['snippet']['textDisplay']
       comentarios.append(comentario)
    return comentarios

url = input("Introduce el link del video de YouTube a analizar ") #Ejemplo https://www.youtube.com/watch?v=AIYpdjQVidc
partes = url.split("=")
video_id= partes[1].split("&")[0]
print(video_id)
comentarios_recientes = obtener_comentarios_recientes(video_id)
#print(comentarios_recientes) 
print(f"Comentarios recientes (formato): {type(comentarios_recientes)}")
print(f"Primer comentario: {comentarios_recientes[0] if comentarios_recientes else 'No hay comentarios'}")


#print(data)
import pandas as pd
def analizar_comentarios(comentarios, model_id, api_token):
    all_data=[]
    for string in comentarios:
        data = query(string, model_id, api_token)  # Ejecutar la consulta de análisis de sentimientos
        print(data)       
        for item in data:
                all_data.append(item)
            # Pausa de 1 segundo para reducir la tasa de solicitudes
            time.sleep(1)
        

    df = pd.DataFrame(all_data)
    total_comentarios= len(df)/3
     
     #Suma de los datos
    positivos = df[df['label'] == 'positive']['score'].sum()
    negativos = df[df['label'] == 'negative']['score'].sum()
    neutro = df[df['label'] == 'neutral']['score'].sum()

     #Porcentajes de cada tipo
    p_positivos = positivos / total_comentarios
    p_negativos = negativos / total_comentarios
    p_neutro = neutro / total_comentarios

     #resultados
    print(f"Porcentaje de comentarios positivos: {p_positivos:.2f}%")
    print(f"Porcentaje de comentarios negativos: {p_negativos:.2f}%")
    print(f"Porcentaje de comentarios neutros: {p_neutro:.2f}%")   


analizar_comentarios(comentarios_recientes, model_id, api_token)
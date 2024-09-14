from googleapiclient.discovery import build

#Clave para APIs de Google Cloud
api_key = 'AIzaSyA5Wm4XH80ajTTEHRe57rOYU-XVo1sQK9I'

# URL base de la API de YouTube
youtube = build('youtube', 'v3', developerKey=api_key)


def obtener_comentarios_recientes(video_id, max_results=100):
    comentarios = []
    respuesta = youtube.commentThreads().list(
        part= 'snippet',
        videoId= video_id,
        textFormat= 'plainText',
        maxResults= max_results,
        order= 'time'
    ).execute()
    for item in respuesta['items']:
       comentario = item['snippet']['topLevelComment']['snippet']['textDisplay']
       comentarios.append(comentario)
    return comentarios

video_id ='AIYpdjQVidc'
comentarios_recientes = obtener_comentarios_recientes(video_id)
print(comentarios_recientes)

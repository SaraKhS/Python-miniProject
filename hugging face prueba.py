import requests
def query(payload, model_id, api_token):
	headers = {"Authorization": f"Bearer {api_token}"}
	API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

model_id = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"
api_token = "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" # get yours at hf.co/settings/tokens


'''if isinstance(data, list):
    for result in data:
        # Redondear el score a 2 decimales si existe
        if 'score' in result:
            result['score'] = round(result['score'], 2)'''

#print(data)
import pandas as pd
def analizar_comentarios(comentarios,model_id, api_token):
     all_data=[]
     for string in comentarios:
        data = query(string, model_id, api_token)  
        
        for item in data:
           for result in item:
                result['comment'] = string  # Añadir el comentario original a cada resultado
                all_data.append(result)  # Añadir el resultado completo a la lista


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
    

lista_de_strings = ["qué mal", "me gusta", "me parece una cancion bonita", "es", "genial"]
analizar_comentarios(lista_de_strings, model_id, api_token)
#positivo = 0
#negativo = 0
#neutro = 0
#data = query("qué bien", model_id, api_token)
#print(data) 


'''for item in data[0]:
     if item['label'] == 'positive':
          if round(item['score'],2) > 0.6:
               positivo += 1
     if item['label'] == 'negative':
          if round(item['score'],2) > 0.6:
               negativo += 1
     if item['label'] == 'neutral':
          if round(item['score'],2) > 0.6:
               neutro += 1

total = positivo + negativo + neutro
positivo = (positivo / total)*100
negativo = (negativo / total)*100
neutro = (neutro / total)*100

print("De un total de {total} com")'''

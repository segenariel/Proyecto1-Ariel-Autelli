import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import json_normalize
from fastapi import FastAPI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List

# carga de datos
df_credits = pd.read_csv('credits.csv')
df_dataset = pd.read_csv('dataset.csv')

# funciones

def cantidad_filmaciones_mes(mes: str) -> str:
    mes_numero = meses.get(mes.lower())
    if mes_numero:
        cantidad = df_dataset[df_dataset['release_date'].dt.month == mes_numero].shape[0]
        return f"{cantidad} cantidad de películas fueron estrenadas en el mes de {mes}"
    else:
        return "Mes no válido"
meses = {
	'enero': 1,
	'febrero': 2,
	'marzo': 3,
	'abril': 4,
	'mayo': 5,
	'junio': 6,
	'julio': 7,
	'agosto': 8,
	'septiembre': 9,
	'octubre': 10,
	'noviembre': 11,
	'diciembre': 12
}

# Convertir la columna 'release_date' al formato datetime
df_dataset['release_date'] = pd.to_datetime(df_dataset['release_date'], errors='coerce')
    

def cantidad_filmaciones_dia(dia: str) -> str:
	# Convertir el nombre del día a minúsculas
	dia = dia.lower()
	
	dias_semana = {
		'lunes': 'Monday',
		'martes': 'Tuesday',
		'miercoles': 'Wednesday',
		'jueves': 'Thursday',
		'viernes': 'Friday',
		'sabado': 'Saturday',
		'domingo': 'Sunday'
	}
	
	dia_ingles = dias_semana.get(dia)
	
	if dia_ingles:
		# Contar la cantidad de filmaciones en el día especificado
		cantidad = df_dataset[df_dataset['release_date'].dt.day_name() == dia_ingles].shape[0]
		return f"{cantidad} cantidad de películas que fueron estrenadas el día {dia}"
	else:
		return "Día no válido"
    
    
def score_titulo(titulo_de_la_filmacion: str) -> str:
    # Filtrar el dataframe por el título de la filmación
    filmacion = df_dataset[df_dataset['title'].str.lower() == titulo_de_la_filmacion.lower()]
    
    if not filmacion.empty:
        # Obtener el año de estreno y el score/popularidad
        titulo = filmacion['title'].values[0]
        anio_estreno = int(filmacion['release_year'].values[0])
        score = filmacion['popularity'].values[0]
        
        return f"La película {titulo} fue estrenada en el año {anio_estreno} con una popularidad de {score}."
    else:
        return "No se encontró la película con el título proporcionado."
    
def votos_titulo(titulo_de_la_filmacion: str) -> str:
    # Filtrar el dataframe por el título de la filmación
    filmacion = df_dataset[df_dataset['title'].str.lower() == titulo_de_la_filmacion.lower()]
    
    if not filmacion.empty:
        # Obtener la cantidad de votos y el valor promedio de las votaciones
        titulo = filmacion['title'].values[0]
        cantidad_votos = int(filmacion['vote_count'].values[0])
        promedio_votos = filmacion['vote_average'].values[0]
        
        # Verificar si la cantidad de votos es al menos 2000
        if cantidad_votos >= 2000:
            return f"La película {titulo} tiene {cantidad_votos} votos con un promedio de {promedio_votos}."
        else:
            return "La película no cumple con la condición de tener al menos 2000 valoraciones, no se devuelve ningún valor."
    else:
        return "No se encontró la película con el título proporcionado."
    
def get_actor(nombre_actor: str) -> str:
    # Filtrar el dataframe de créditos para obtener las películas en las que ha participado el actor
    actor_data = credits[credits['cast'].apply(lambda x: any(d['name'].lower() == nombre_actor.lower() for d in eval(x)))]
    
    if not actor_data.empty:
        # Contar la cantidad de películas en las que ha participado el actor
        cantidad_peliculas = actor_data.shape[0]
        
        # Calcular el retorno total y el promedio de retorno
        retorno_total = actor_data['id'].apply(lambda x: df_dataset[df_dataset['id'] == x]['revenue'].values[0] - df_dataset[df_dataset['id'] == x]['budget'].values[0]).sum()
        promedio_retorno = retorno_total / cantidad_peliculas
        
        return f"El actor {nombre_actor} ha participado de {cantidad_peliculas} cantidad de filmaciones, el mismo ha conseguido un retorno de {retorno_total} con un promedio de {promedio_retorno} por filmación."
    else:
        return "No se encontró el actor con el nombre proporcionado."
    
def get_director(nombre_director: str) -> List[dict]:
    # Filtrar el dataframe de créditos para obtener las películas en las que ha trabajado el director
    director_data = credits[credits['crew'].apply(lambda x: any(d['job'] == 'Director' and d['name'].lower() == nombre_director.lower() for d in eval(x)))]
    
    if not director_data.empty:
        peliculas = []
        for idx, row in director_data.iterrows():
            pelicula = df_dataset[df_dataset['id'] == row['id']]
            if not pelicula.empty:
                titulo = pelicula['title'].values[0]
                fecha_lanzamiento = pelicula['release_date'].values[0]
                costo = pelicula['budget'].values[0]
                ganancia = pelicula['revenue'].values[0]
                retorno_individual = ganancia - costo
                peliculas.append({
                    'titulo': titulo,
                    'fecha_lanzamiento': fecha_lanzamiento,
                    'retorno_individual': retorno_individual,
                    'costo': costo,
                    'ganancia': ganancia
                })
        return peliculas
    else:
        return "No se encontró el director con el nombre proporcionado."

def recomendacion(titulo: str) -> List[str]:
    # Vectorizar los títulos de las películas
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(df_dataset['title'].fillna(''))
    
    # Calcular la similitud coseno entre las películas
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    # Obtener el índice de la película que coincide con el título dado
    idx = df_dataset[df_dataset['title'].str.lower() == titulo.lower()].index[0]
    
    # Obtener las puntuaciones de similitud de todas las películas con la película dada
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Ordenar las películas en función de las puntuaciones de similitud
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Obtener los índices de las 5 películas más similares
    sim_scores = sim_scores[1:6]
    movie_indices = [i[0] for i in sim_scores]
    
    # Devolver los títulos de las 5 películas más similares
    return df_dataset['title'].iloc[movie_indices].tolist()


# end points
app = FastAPI()

@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes: str) -> str:
    mes_numero = meses.get(mes.lower())
    if mes_numero:
        cantidad = df_dataset[df_dataset['release_date'].dt.month == mes_numero].shape[0]
        return f"{cantidad} cantidad de películas fueron estrenadas en el mes de {mes}"
    else:
        return "Mes no válido"

@app.get('/cantidad_filmaciones_dia/{dia}')
def cantidad_filmaciones_dia(dia: str) -> str:
    dia = dia.lower()
    dias_semana = {
        'lunes': 'Monday',
        'martes': 'Tuesday',
        'miercoles': 'Wednesday',
        'jueves': 'Thursday',
        'viernes': 'Friday',
        'sabado': 'Saturday',
        'domingo': 'Sunday'
    }
    dia_ingles = dias_semana.get(dia)
    if dia_ingles:
        cantidad = df_dataset[df_dataset['release_date'].dt.day_name() == dia_ingles].shape[0]
        return f"{cantidad} cantidad de películas fueron estrenadas el día {dia}"
    else:
        return "Día no válido"

@app.get('/score_titulo/{titulo_de_la_filmacion}')
def score_titulo(titulo_de_la_filmacion: str) -> str:
    filmacion = df_dataset[df_dataset['title'].str.lower() == titulo_de_la_filmacion.lower()]
    if not filmacion.empty:
        titulo = filmacion['title'].values[0]
        anio_estreno = int(filmacion['release_year'].values[0])
        score = filmacion['popularity'].values[0]
        return f"La película {titulo} fue estrenada en el año {anio_estreno} con una popularidad de {score}."
    else:
        return "No se encontró la película con el título proporcionado."

@app.get('/votos_titulo/{titulo_de_la_filmacion}')
def votos_titulo(titulo_de_la_filmacion: str) -> str:
    filmacion = df_dataset[df_dataset['title'].str.lower() == titulo_de_la_filmacion.lower()]
    if not filmacion.empty:
        titulo = filmacion['title'].values[0]
        cantidad_votos = int(filmacion['vote_count'].values[0])
        promedio_votos = filmacion['vote_average'].values[0]
        if cantidad_votos >= 2000:
            return f"La película {titulo} tiene {cantidad_votos} votos con un promedio de {promedio_votos}."
        else:
            return "La película no cumple con la condición de tener al menos 2000 valoraciones, no se devuelve ningún valor."
    else:
        return "No se encontró la película con el título proporcionado."

@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor: str) -> str:
    actor_data = credits[credits['cast'].apply(lambda x: any(d['name'].lower() == nombre_actor.lower() for d in eval(x)))]
    if not actor_data.empty:
        cantidad_peliculas = actor_data.shape[0]
        retorno_total = actor_data['id'].apply(lambda x: df_dataset[df_dataset['id'] == x]['revenue'].values[0] - df_dataset[df_dataset['id'] == x]['budget'].values[0]).sum()
        promedio_retorno = retorno_total / cantidad_peliculas
        return f"El actor {nombre_actor} ha participado de {cantidad_peliculas} cantidad de filmaciones, el mismo ha conseguido un retorno de {retorno_total} con un promedio de {promedio_retorno} por filmación."
    else:
        return "No se encontró el actor con el nombre proporcionado."

@app.get('/get_director/{nombre_director}')
def get_director(nombre_director: str) -> List[dict]:
    director_data = credits[credits['crew'].apply(lambda x: any(d['job'] == 'Director' and d['name'].lower() == nombre_director.lower() for d in eval(x)))]
    if not director_data.empty:
        peliculas = []
        for idx, row in director_data.iterrows():
            pelicula = df_dataset[df_dataset['id'] == row['id']]
            if not pelicula.empty:
                titulo = pelicula['title'].values[0]
                fecha_lanzamiento = pelicula['release_date'].values[0]
                retorno_individual = pelicula['revenue'].values[0] - pelicula['budget'].values[0]
                costo = pelicula['budget'].values[0]
                ganancia = pelicula['revenue'].values[0]
                peliculas.append({
                    'titulo': titulo,
                    'fecha_lanzamiento': fecha_lanzamiento,
                    'retorno_individual': retorno_individual,
                    'costo': costo,
                    'ganancia': ganancia
                })
        return peliculas
    else:
        return "No se encontró el director con el nombre proporcionado."
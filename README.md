# PROYECTO INDIVIDUAL 1 - Agregador de Plataformas de Streaming

**Autor:** Ariel Adrian Autelli
**Cohorte:** datapt12

## Descripción General

Este proyecto consistió en el desarrollo de un MVP para una empresa que provee servicios de agregación de plataformas de streaming. Los objetivos principales fueron:

* **Transformación de Datos:** Limpieza y preparación de los datasets para su análisis.
* **Análisis Exploratorio de Datos (EDA):** Obtención de insights relevantes para el sistema de recomendación y la API.
* **Desarrollo de una API:** Creación de endpoints para consultar información sobre películas, directores y actores.
* **Implementación de un Sistema de Recomendación:** Desarrollo de un modelo basado en filtrado de contenido por género.

## Transformaciones de Datos

### Dataset 1: Créditos de las películas

* Debido al gran tamaño de este dataset, se realizó un **proceso de análisis y transformación previo** en un código aparte. El objetivo fue extraer únicamente la información necesaria para este proyecto, permitiendo su manejo eficiente y deployment en plataformas como Render.

### Dataset 2: Información de las películas

Se aplicaron las siguientes transformaciones específicas a este dataset:

* **Desanidación de columnas:** `belongs_to_collection` y `production_companies` fueron expandidas para facilitar el acceso a sus datos internos.
* **Imputación de valores nulos:** Los campos `revenue` y `budget` fueron rellenados con el valor `0` en caso de ausencia de datos.
* **Eliminación de valores nulos:** Se eliminaron las filas con valores nulos en la columna `release_date` debido a su importancia.
* **Formato de fechas y extracción del año:** La columna `release_date` se formateó a `AAAA-MM-DD`, y se creó una nueva columna `release_year` con el año de estreno.
* **Cálculo del retorno de inversión:** Se generó la columna `return` calculada como `revenue / budget`. En caso de división por cero o datos no disponibles, se asignó el valor `0`.
* **Eliminación de columnas innecesarias:** Se eliminaron las columnas `video`, `imdb_id`, `adult`, `original_title`, `poster_path` y `homepage` por no ser relevantes para los objetivos del proyecto.

## Análisis Exploratorio de Datos (EDA)

Tras la limpieza y transformación de los datos, se llevó a cabo un análisis exploratorio para identificar patrones y obtener información valiosa para el desarrollo de la API y el sistema de recomendación. Los principales análisis realizados fueron:

1.  **Tendencia de películas estrenadas por año:** Visualización de la cantidad de películas lanzadas a lo largo del tiempo.
2.  **Presupuesto promedio por año:** Análisis de la evolución del presupuesto promedio de las películas por año.
3.  **Nube de palabras con las palabras más frecuentes en los títulos:** Identificación de los términos más comunes en los títulos de las películas.

## API

Se desarrollaron los siguientes 6 endpoints obligatorios utilizando una framework como FastAPI (asumiendo esto por la mención de Render y prácticas modernas):

1.  **`/peliculas_mes/{mes}`:**
    * **Descripción:** Retorna la cantidad de películas estrenadas en el mes ingresado (en español).
    * **Ejemplo:** `/peliculas_mes/enero` -> `{"cantidad": 150}`

2.  **`/peliculas_dia/{dia}`:**
    * **Descripción:** Retorna la cantidad de películas estrenadas en el día de la semana ingresado (en español).
    * **Ejemplo:** `/peliculas_dia/lunes` -> `{"cantidad": 85}`

3.  **`/pelicula_info/{titulo_pelicula}`:**
    * **Descripción:** Retorna el título, año de estreno y score de la película ingresada.
    * **Ejemplo:** `/pelicula_info/Titanic` -> `{"titulo": "Titanic", "anio_estreno": 1997, "score": 7.8}`

4.  **`/director_info/{nombre_director}`:**
    * **Descripción:** Retorna información detallada sobre un director.
    * **Respuesta:**
        * `exito_director`: Retorno promedio de todas las películas dirigidas por el director.
        * `peliculas`: Lista de películas dirigidas, incluyendo:
            * `titulo`: Título de la película.
            * `fecha_lanzamiento`: Fecha de lanzamiento (AAAA-MM-DD).
            * `retorno_individual`: Retorno de inversión de la película.
            * `costo`: Presupuesto de la película.
            * `ganancia`: Ganancia de la película (revenue - budget).
    * **Ejemplo:** `/director_info/James Cameron` -> `{"exito_director": 8.5, "peliculas": [...]}`

5.  **`/actor_info/{nombre_actor}`:**
    * **Descripción:** Retorna información sobre un actor.
    * **Respuesta:**
        * `exito_actor`: Retorno promedio de las películas en las que participó (sin incluir las que dirigió).
        * `cantidad_peliculas`: Número total de películas en las que ha participado.
        * `retorno_promedio`: Promedio del retorno de inversión de sus películas (excluyendo las dirigidas).
    * **Ejemplo:** `/actor_info/Leonardo DiCaprio` -> `{"exito_actor": 7.2, "cantidad_peliculas": 35, "retorno_promedio": 6.9}`

## Sistema de Recomendación

El sistema de recomendación implementado utiliza un enfoque de **filtrado de contenido** basado en los **géneros** de las películas.

* La función `recomendacion(titulo_pelicula)` toma como entrada el título de una película.
* Retorna las **cinco películas más similares** en función de sus géneros, excluyendo la película original ingresada.
* Este método permite ofrecer recomendaciones personalizadas a los usuarios basadas en sus preferencias de género.

```python
# Ejemplo de cómo usar la función de recomendación (esto iría en el código de la API o en un notebook de ejemplo)
# from sistema_recomendacion import recomendacion

# recomendaciones = recomendacion("The Dark Knight")
# print(recomendaciones)
# # Output: ["Batman Begins", "Batman Returns", "Batman Forever", "Batman & Robin", "Watchmen"]

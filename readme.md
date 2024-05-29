# <h1 align = center> **Proyecto Individual Nº1: MLOps** <h1>
Machine Learning Operations (MLOps)
Introducción
En este proyecto, exploramos el mundo de las Operaciones de Machine Learning (MLOps) a través de tres etapas fundamentales: Preparación de Datos, Análisis Exploratorio de Datos (EDA) y Aplicación de Técnicas de Machine Learning. Utilizamos datos de la plataforma de juegos Steam, una comunidad con millones de usuarios.

# <h2>Descripción del Proyecto<h2>

1. Preparación de Datos (ETL)
Actuando como Ingenieros de Datos, llevamos a cabo un proceso de Extracción, Transformación y Carga (ETL), que se puede ver en detalle en el notebook ETL. En esta fase, limpiamos tres conjuntos de datos, eliminando valores nulos y columnas irrelevantes, y creamos una nueva columna "sentiment_analysis" basada en las recomendaciones de los usuarios. Esto preparó nuestros datos para las siguientes etapas del proyecto.

2. Creación de una API con FastAPI
Usamos nuestras habilidades en preparación de datos para desarrollar una API con FastAPI. Esta API permite una interacción eficiente con nuestros datos y está alojada en un servidor de Render para facilitar su acceso. Las funciones de la API permiten consultar datos como la cantidad de ítems y el porcentaje de contenido gratuito por año según la empresa desarrolladora, el gasto de los usuarios y el porcentaje de recomendación basado en las reseñas. Puedes ver más detalles en funciones.py.

3. Análisis Exploratorio de Datos (EDA)
En esta etapa, limpiamos y exploramos los datos para prepararlos para futuras predicciones. Realizamos un análisis exploratorio (EDA) para entender las relaciones entre variables, detectar patrones e identificar posibles anomalías. Este análisis se detalla en el cuaderno EDA.

4. Modelo Predictivo
Finalmente, entrenamos un modelo de aprendizaje automático para recomendar juegos a los usuarios utilizando técnicas de filtrado colaborativo con la biblioteca "surprise". Este proceso se documenta en el cuaderno machine. También preparamos un video que demuestra el funcionamiento de las funciones de la API, facilitando la comprensión y el acceso a nuestros resultados.

Este proyecto nos ha permitido adquirir habilidades clave en MLOps, desde la preparación y análisis de datos hasta la implementación de un modelo predictivo para recomendaciones de juegos en Steam.



# <h1>Funciones Disponibles<h1>

**developer( desarrollador : str )**:  Proporciona la cantidad de ítems y el porcentaje de contenido gratuito por año para una empresa desarrolladora específica.


**userdata( User_id : str )**: Devuelve el total de dinero gastado por el usuario, el porcentaje de recomendaciones positivas y la cantidad de ítems adquiridos.


**best_developer_year(año: int)**: Identifica los tres desarrolladores con los juegos más recomendados por los usuarios en un año específico.


**developer_reviews_analysis(desarrolladora: str)**: Devuelve un resumen de las reseñas de usuarios (positivas y negativas) para una desarrolladora específica.


**user_recommendations(user_id: str)**: Proporciona una lista de cinco juegos recomendados para un usuario específico basado en sus preferencias y actividad.

**UserForGenre(genre: str)**: Proporciona información del usuario con más horas jugadas en un género específico



Despliegue: La API se ha desplegado utilizando Render para facilitar su acceso y consulta desde la web.

# <h2>Análisis Exploratorio de Datos (EDA)<h2>
Después de limpiar los datos, investigamos las relaciones entre variables, identificamos outliers y detectamos patrones interesantes. Este análisis nos ayudó a comprender mejor nuestros datos y prepararlos para el modelo predictivo. Realizamos tanto análisis univariados como multivariados para estudiar la distribución y las relaciones entre las columnas.

# <h2>Modelo de Predicción<h2>
La API facilita el uso de datos por parte de los departamentos de análisis y machine learning. Entrenamos un modelo de recomendación con "surprise" para predecir juegos que podrían interesar a los usuarios. El modelo, exportado como un archivo .pkl, puede ser utilizado en el script principal para generar recomendaciones personalizadas.


Nombre del Autor: Celada Juan Cruz
Email: Juan.celada123@gmail.com 
GitHub: https://github.com/juancelada
LinkedIn: https://www.linkedin.com/in/juan-cruz-celada/


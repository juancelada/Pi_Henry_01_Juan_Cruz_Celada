import pandas as pd
import pyarrow.parquet as pq
import pickle
from fastapi import FastAPI

# Inicializar FastAPI
app = FastAPI()

# Cargar los DataFrames
try:
    games = pd.read_parquet("games.parquet")
    items = pd.read_parquet("items.parquet")
    reviews = pd.read_parquet("reviews.parquet")
except Exception as e:
    print(f"Error al cargar los DataFrames: {e}")

# Cargar el modelo y el DataFrame asociado
try:
    with open('model.pkl', 'rb') as archivo:
        model = pickle.load(archivo)
    model_df = pd.read_parquet('model.parquet')
except Exception as e:
    print(f"Error al cargar el modelo o el DataFrame del modelo: {e}")

# Función para obtener una descripción del desarrollador del juego
def developer(dev: str):
    if dev not in games['developer'].unique():
        return {'error': 'El Desarrollador especificado no existe.'}
    
    # Filtra los juegos del desarrollador especificado
    developer_data = games[games["developer"] == dev]
    
    # Cuenta la cantidad de juegos por año
    cantidad_item = developer_data.groupby("release_year")["item_id"].count()
    
    # Filtra los juegos gratuitos
    gratis = developer_data[developer_data["price"] == 0]
    
    # Cuenta los juegos gratuitos por año
    total_gratis = gratis.groupby("release_year")["price"].count()
    
    # Calcula el porcentaje de juegos gratuitos por año
    cont_gratis_año = round((total_gratis / cantidad_item) * 100, 2)
    
    # Asigna nombres a las series de datos
    cantidad_item.name = "number of items"
    cont_gratis_año.name = "Free content"
    
    # Combina las series en un DataFrame y rellena valores NaN con 0
    tabla = pd.merge(cantidad_item, cont_gratis_año, on="release_year").reset_index()
    tabla = tabla.fillna(0)
    
    # Formatea el contenido gratuito como porcentaje
    tabla["Free content"] = tabla["Free content"].apply(lambda x: f"{x}%")
    
    # Convierte el DataFrame a un diccionario
    diccionario = tabla.to_dict(orient="records")
    return diccionario

# Función para obtener una breve descripción sobre la cuenta de un usuario
def userdata(user_id: str):
    merged_reviews_games = reviews.merge(games[['item_id', 'price']], left_on="item_id", right_on="item_id")
    merged_reviews_games.drop(columns=['helpful', 'año', "sentiment_analysis"], inplace=True)
    
    if user_id not in merged_reviews_games['user_id'].unique():
        return {'error': 'El usuario especificado no existe.'}
    
    # Filtra los datos para el usuario especificado
    user_data = merged_reviews_games[merged_reviews_games['user_id'] == user_id]
    
    # Calcula la cantidad de dinero gastado por el usuario
    dinero_gastado = user_data['price'].sum()
    
    # Calcula el porcentaje de recomendación en base a reviews.recommend
    recomendacion = user_data['recommend'].sum()
    porcentaje_recomendacion = recomendacion / len(user_data) * 100
    
    # Calcula la cantidad de items
    cantidad_de_items = user_data['item_id'].nunique()
    
    # Crea un diccionario con los resultados
    resultados = {
        'Cantidad de dinero gastado': dinero_gastado,
        'Porcentaje de recomendación': porcentaje_recomendacion,
        'Cantidad de items': cantidad_de_items
    }
    return resultados

# Función para obtener información del usuario con más horas jugadas en un género específico
def UserForGenre(genre: str):
    merged_items_games = pd.merge(games, items, left_on="item_id", right_on="item_id")
    
    if genre not in merged_items_games.columns:
        return {'error': f"El género {genre} no existe en la base de datos."}
    
    # Filtra los juegos del género especificado
    df_genero = merged_items_games[merged_items_games[genre] == 1]
    
    # Encuentra el usuario con más horas jugadas en el género
    usur_mas_horas = df_genero.groupby("user_id")["playtime_forever"].sum().idxmax()
    
    # Filtra los datos del usuario con más horas jugadas
    filtro_usuario = df_genero[df_genero["user_id"] == usur_mas_horas]
    
    # Calcula las horas jugadas por año
    horas_jugadas_año = filtro_usuario.groupby("release_year")["playtime_forever"].sum()
    
    # Convierte los datos a un diccionario
    registro = horas_jugadas_año.to_dict()
    Horas_por_año = {f'Año: {int(clave)}': int(valor) for clave, valor in registro.items()}
    
    return {"Usuario con más horas jugadas": usur_mas_horas, "Horas jugadas por año": Horas_por_año}

# Función para obtener los mejores desarrolladores de un año específico
def best_developer_year(year: int):
    merged_df = reviews.merge(games, left_on="item_id", right_on="item_id")
    
    if year not in merged_df['año'].unique():
        return {'error': 'El año especificado no existe.'}
    
    # Filtra los juegos por año y por recomendación positiva
    df_year = merged_df[(merged_df['año'] == year) & (merged_df['recommend'] == True) & (merged_df['sentiment_analysis'] == 2)]
    
    # Cuenta el número de juegos recomendados por desarrollador y devuelve los tres primeros desarrolladores
    top_desarrolladores = df_year['developer'].value_counts().head(3).index.tolist()
    
    return {"Puesto 1": top_desarrolladores[0], "Puesto 2": top_desarrolladores[1], "Puesto 3": top_desarrolladores[2]}

# Función para analizar las reviews de un desarrollador
def developer_reviews_analysis(developer: str):
    merged = reviews.merge(games, left_on="item_id", right_on="item_id")
    
    if developer not in games['developer'].unique():
        return {'error': 'El Desarrollador especificado no existe.'}
    
    # Filtra las columnas a utilizar
    df = merged[['user_id', 'item_id', 'developer', 'año', 'sentiment_analysis']]
    
    # Filtra los datos por desarrolladora
    df_merged = df[df["developer"] == developer]
    
    # Obtiene la cantidad de reviews positivas y negativas
    reviews_positivas = df_merged[df_merged["sentiment_analysis"] == 2].shape[0]
    reviews_negativas = df_merged[df_merged["sentiment_analysis"] == 0].shape[0]
    
    # Crea un string con el resumen de las reviews
    resumen_reviews = f"[Negative = {reviews_negativas}, Positive = {reviews_positivas}]"
    
    # Crea un diccionario con los resultados obtenidos
    dicc = {developer: resumen_reviews}
    
    return dicc

# Función para obtener recomendaciones de juegos para un usuario
def user_recomendations(user_id: str):
    if user_id not in model_df['user_id'].unique():
        return {'error': 'El usuario no existe.'}
    
    # Obtiene los juegos que el usuario ya ha valorado
    games_val = model_df[model_df['user_id'] == user_id]['app_name'].unique()
    
    # Obtiene todos los juegos en el modelo
    all_games = model_df['app_name'].unique()
    
    # Encuentra los juegos que el usuario no ha valorado
    games_no_val = list(set(all_games) - set(games_val))
    
    # Predice las valoraciones para los juegos no valorados
    predictions = [model.predict(user_id, game) for game in games_no_val]
    
    # Ordena las predicciones y obtiene las 5 mejores recomendaciones
    recomendations = sorted(predictions, key=lambda x: x.est, reverse=True)[:5]
    games_recomend = [recomendation.iid for recomendation in recomendations]
    
    # Crea un diccionario con las recomendaciones
    recomendations_dict = {f"game {i+1}": games_recomend[i] for i in range(5)}
    
    return recomendations_dict

id
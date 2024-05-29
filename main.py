from fastapi import FastAPI
from typing import Union
from funciones import developer
from funciones import userdata
from funciones import UserForGenre
from funciones import best_developer_year  
from funciones import  developer_reviews_analysis
from funciones import user_recomendations
from fastapi.responses import JSONResponse
from typing import List, Dict, Tuple, Sequence, Any, Union, Optional, Callable
app = FastAPI()

#END POINTS

@app.get("/developer/{dev}")
async def get_developer(dev: str):
    try:
        resultado = developer(dev)
        return resultado
    except Exception as e:
        return {"error": str(e)}

@app.get("/userdata/{user_id}")
async def get_user(user_id: str):
    try:
        result = userdata(user_id)
        return result
    except Exception as e:
        return {"error": str(e)}

@app.get("/UserForGenre/{genre}")
async def get_UserForGenre(genre: str):
    try:
        resultado = UserForGenre(genre)
        return resultado
    except Exception as e:
        return {"error": str(e)}

@app.get("/best_developer_year/{year}")
async def get_best_developer_year(year: int):
    try:
        result = best_developer_year(year)
        return result
    except Exception as e:
        return {"error": str(e)}

@app.get("/developer_reviews_analysis/{developer}")
async def get_developer_reviews_analysis(developer: str):
    try:
        resultado = developer_reviews_analysis(developer)
        return resultado
    except Exception as e:
        return {"error": str(e)}

@app.get("/user_recomendations/{user_id}")
async def get_user_recommendations(user_id: str):
    try:
        resultado = user_recomendations(user_id)
        return resultado
    except Exception as e:
        return {"error": str(e)}
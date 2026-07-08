# версия в висуалстудио - июль 2026
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import forms  # Импортируем наш новый роутер
from routers import test2  # Импортируем роутер test2
from routers import test3  # Импортируем роутер test2



app = FastAPI()

# Подключаем роутер форм к главному приложению
app.include_router(forms.router, tags=["роутер 1 - без префикса"])
app.include_router(test2.router2 , prefix="/test", tags=["роутер 2"] )
app.include_router(test3.router3 , prefix="/test3", tags=["роутер 3"] )


# Здесь можно монтировать статику, если она у вас есть:
app.mount("/static", StaticFiles(directory="static"), name="static")

FILE_PATH = os.path.join(os.path.dirname(__file__), "val.txt")

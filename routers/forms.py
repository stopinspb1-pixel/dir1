import os
from dotenv import load_dotenv
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

load_dotenv()

# Создаем изолированный роутер вместо app
router = APIRouter()

# Настраиваем шаблоны (указываем правильный путь, поднявшись на уровень выше)
templates = Jinja2Templates(directory="templates")

def get_site_urls():
    return {
        "url_A": os.getenv("SITE_A", "#"),
        "url_B": os.getenv("SITE_B", "#"),
        "url_C": os.getenv("SITE_C", "#"),
        "url_D": os.getenv("SITE_D", "#"),
        "url_E": os.getenv("SITE_E", "#"),
        "url_F": os.getenv("SITE_F", "#"),
        "url_G": os.getenv("SITE_G", "#"),
        "url_H": os.getenv("SITE_H", "#"),
        "url_J": os.getenv("SITE_J", "#"),
    }

# Обратите внимание: теперь пишем @router вместо @app
@router.get("/3", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="gena.htm", 
        context={"username": "Геннадий", "status": "Админ", **get_site_urls()}
    )

@router.post("/3", response_class=HTMLResponse)
async def handle_form(
    request: Request, 
    button_action: str = Form(...),
    user_text: str = Form("") 
):
    if button_action == "btn1":
        message = "Ура, Вы нажали Первую кнопку!"
    elif button_action == "btn2":
        message = "Вы нажали Вторую кнопку!"
    elif button_action == "btn3":
        message = "Вы нажали Третью кнопку!"
    else:
        message = "Вы отправили текст нажатием клавиши Enter!"

    if user_text.strip():
        message2 = f"Вы ввели текст: {user_text}"
    else:
        message2 = "Вы ничего не ввели в текстовое поле."

    return templates.TemplateResponse(
        request=request, 
        name="gena.htm", 
        context={
            "username": "Геннадий", 
            "status": "Админ", 
            "message": message,
            "message2": message2,
            "user_text": user_text,
            **get_site_urls()
        }
    )

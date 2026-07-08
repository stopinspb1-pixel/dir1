import os
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

# Переменная роутера строго совпадает с router3 из main.py
router3 = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
LOG_FILE_PATH = os.path.join(BASE_DIR, "val.txt")

# GET-метод: панель управления лог-файлом (http://localhost:8020/test3/manage)
@router3.get("/manage", response_class=HTMLResponse)
async def manage_logs_page(request: Request):
    # Считаем размер файла для вывода информации
    file_size = 0
    if os.path.exists(LOG_FILE_PATH):
        file_size = os.path.getsize(LOG_FILE_PATH)
        
    return templates.TemplateResponse(
        request=request,
        name="manage_logs.htm",
        context={
            "page_title": "Управление файлом val.txt",
            "file_size": file_size,
            "file_path": LOG_FILE_PATH
        }
    )

# POST-метод: обработка команды на полную очистку файла
@router3.post("/clear", response_class=HTMLResponse)
async def clear_log_file(request: Request):
    try:
        # Открытие файла в режиме 'w' полностью стирает его содержимое
        with open(LOG_FILE_PATH, "w", encoding="utf-8") as f:
            f.write("") 
        
        # После очистки перенаправляем пользователя обратно на страницу статуса (роутер 2)
        # чтобы он сразу увидел пустой лог
        return RedirectResponse(url="/test/status", status_code=303)
    except Exception as e:
        return HTMLResponse(content=f"Ошибка при очистке файла: {str(e)}", status_code=500)

import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router2 = APIRouter()

# Рассчитываем путь к папке templates и к файлу val.txt относительно папки routers
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
LOG_FILE_PATH = os.path.join(BASE_DIR, "val.txt")

# Функция чтения логов
def read_logs():
    if not os.path.exists(LOG_FILE_PATH):
        return ["Файл val.txt еще не создан."]
    try:
        with open(LOG_FILE_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
            return [line.strip() for line in lines[-100:]]  # Возвращаем последние 100 строк
    except Exception as e:
        return [f"Ошибка чтения файла: {str(e)}"]

# Этот эндпоинт будет доступен по адресу /test/status
@router2.get("/status", response_class=HTMLResponse)
async def show_status_page(request: Request):
    log_lines = read_logs()
    
    # Возвращаем новый шаблон, передавая туда список строк из файла
    return templates.TemplateResponse(
        request=request,
        name="status.htm",
        context={
            "page_title": "Системный статус и логи",
            "logs": log_lines
        }
    )

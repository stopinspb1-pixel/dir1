FROM python:3.11-slim

WORKDIR /app

RUN pip install fastapi uvicorn jinja2 python-multipart python-dotenv

COPY main.py .
COPY templates/ templates/
COPY val.txt .

EXPOSE 8020

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8020"]

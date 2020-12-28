FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY . .

RUN pip install -r requirements.txt

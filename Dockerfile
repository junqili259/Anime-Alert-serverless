FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./api .

RUN pip install -r requirements.txt

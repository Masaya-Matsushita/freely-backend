FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

FROM --platform=linux/x86_64 freely-backend

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app/app

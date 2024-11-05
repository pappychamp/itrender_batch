# ベースステージ
FROM python:3.12.3-alpine3.20 AS base
RUN mkdir /app
WORKDIR /app
COPY ./task/app/ .

# devステージ
FROM base AS dev
COPY requirements/dev.txt ./requirements.txt
RUN pip install -r requirements.txt
CMD ["python", "/app/function.py"]

# prodステージ
FROM base AS prod
COPY requirements/prod.txt ./requirements.txt
RUN pip install -r requirements.txt
CMD ["python", "/app/function.py"]

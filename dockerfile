FROM python:3.12.3-alpine3.20
RUN mkdir /app
WORKDIR /app
COPY requirements/prod.txt ./requirements.txt
COPY ./task/app/ .

RUN pip install -r requirements.txt 

CMD ["python","/app/function.py"]

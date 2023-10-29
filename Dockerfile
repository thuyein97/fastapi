FROM python:3.9.7

WORKDIR /usr/app/src

COPY requirements.txt ./

RUN apt update

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000"]


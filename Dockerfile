FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN pip3 install aitextgen

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
FROM python:3.9

#RUN apk --update add git g++
RUN apt-get install git

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --upgrade pip
RUN python -m pip install --upgrade setuptools
RUN pip install -r requirements.txt
RUN python -m pip install git+https://github.com/sid-viscous/DiscordHandler

COPY . /app

WORKDIR /app/bot

CMD ["python3", "/app/bot/main.py"]
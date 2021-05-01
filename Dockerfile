FROM python:3.9-alpine

RUN apk --update add git

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN python -m pip install git+https://github.com/sid-viscous/DiscordHandler

COPY . /app

WORKDIR /app/bot

CMD ["python3", "/app/bot/main.py"]
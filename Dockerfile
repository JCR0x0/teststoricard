FROM python:3

COPY ["app.py", "stori.jpg", "./"]

ADD ./mountdir /mountdir

CMD [ "python", "./app.py" ]

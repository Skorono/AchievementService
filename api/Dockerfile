
FROM python:3.12-slim-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY .. .

ENV FLASK_APP=api/app.py
ENV PYTHONPATH "${PYTHONPATH}:/app"

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
FROM python:3.7

WORKDIR /src

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# ENTRYPOINT ["gunicorn","--bind","0.0.0.0:5000","wsgi:app"]
ENTRYPOINT ["python", "app.py"]

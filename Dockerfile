FROM python:3.7-alpine
WORKDIR /usr/src

EXPOSE 5000
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["gunicorn", "--workers=2", "--bind=0.0.0.0:5000", "app:app"]
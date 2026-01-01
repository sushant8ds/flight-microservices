FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .
COPY Data /app/Data

EXPOSE 8002
CMD ["python", "manage.py", "runserver", "0.0.0.0:8002"]

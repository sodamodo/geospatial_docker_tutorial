FROM python:3.6
WORKDIR /app
COPY backend /app/backend/
COPY manage.py requirements.txt /app/
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

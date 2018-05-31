FROM python:3.6
ENV CACHEBUSTER=1111111

WORKDIR /app
COPY backend /app/backend/
COPY manage.py requirements.txt /app/
RUN pip install -r requirements.txt
EXPOSE 8000
RUN python manage.py collectstatic --no-input
RUN echo static collected
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

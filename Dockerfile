FROM python:3.7-slim
LABEL MAINTAINER="Neil Kuan"
LABEL NAME="flask-upload"
LABEL Version="v0.0.6"
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt --no-cache-dir
EXPOSE 8080
CMD ["python", "app.py"]

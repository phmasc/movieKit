FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    pip install moviepy flask

WORKDIR /app
COPY app.py .
EXPOSE 5000

CMD ["python", "app.py"]

FROM python:3.12-slim
WORKDIR /app
COPY us.py .
RUN pip install --no-cache-dir flask requests
EXPOSE 8080
CMD ["python", "us.py"]
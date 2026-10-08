FROM python:3.12-slim
WORKDIR /app
COPY fs.py .
RUN pip install --no-cache-dir flask
EXPOSE 9090
CMD ["python", "fs.py"]
FROM python:3.10
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 3000
CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "3000"]

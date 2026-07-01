FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . ./langchain_project

EXPOSE 8000

ENV PYTHONPATH=/app

CMD ["fastapi", "run", "langchain_project/main.py", "--host", "0.0.0.0", "--port", "8000"]
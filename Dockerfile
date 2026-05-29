
FROM python:3.14

WORKDIR /first_project


COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

EXPOSE 8000
CMD ["fastapi", "run", "main.py","--host", "0.0.0.0", "--port", "8000"]
FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY python/. .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# syntax=docker/dockerfile:1
FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code

RUN apk add --no-cache gcc musl-dev libffi-dev python3-dev openssl-dev sqlite sqlite-libs


# Install dependencies
RUN pip install --upgrade pip

COPY requirements.txt /code/
RUN pip install wheel
RUN pip install -r requirements.txt
COPY . /code/


# Expose the FastAPI default port
EXPOSE 8000

# # Command to run the FastAPI application
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


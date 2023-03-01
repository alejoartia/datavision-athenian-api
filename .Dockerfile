# Use a smaller base image
FROM python:3.9-alpine as build

# Specify the version of Python
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /code

# Install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev openssl-dev \
    && pip install --no-cache-dir --upgrade -r /code/requirements.txt \
    && apk del .build-deps

# Copy the application code
COPY ./app /code/app

# Separate the build and run steps
FROM python:3.9-alpine as run
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY --from=build /usr/local/lib/python3.9 /usr/local/lib/python3.9
COPY --from=build /code/app /app

# Set environment variables
ENV HOST=0.0.0.0 PORT=15400

# Start the application
CMD ["uvicorn", "index:app", "--host", "${HOST}", "--port", "${PORT}"]
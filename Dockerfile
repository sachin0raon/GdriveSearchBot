FROM python:3.9.0-slim
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN ["pip", "install", "--no-cache-dir", "-r", "requirements.txt"]
ENTRYPOINT ["python", "-u", "main.py"]
FROM python:3.8-slim-buster
WORKDIR ./
COPY . /app
WORKDIR /app

RUN /usr/local/bin/python -m pip install --upgrade pip && pip3 install -r requirements.txt
EXPOSE 8080
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8080"]
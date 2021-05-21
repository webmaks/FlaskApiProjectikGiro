#FROM python:3.7-alpine
FROM python:3.8-slim-buster
#WORKDIR /code
WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0
#RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
#EXPOSE 5000
COPY . .
#CMD ["flask", "run"]
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0" ]


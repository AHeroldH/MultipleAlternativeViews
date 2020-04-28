FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends build-essential r-base python3.7 python3-pip python3-setuptools python3-dev

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt

RUN Rscript -e "install.packages('binostics')"

COPY . /app

EXPOSE 5000

CMD ["python3", "app.py", "--host", "0.0.0.0"]
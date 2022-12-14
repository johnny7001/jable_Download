# FROM python:3.9
FROM python:slim 
WORKDIR /app

COPY . .

# COPY dmmtag_list.txt .
# RUN apk update && apk add gcc \
#                           libc-dev \
#                           libffi-dev
# RUN apt install libcurl4-openssl-dev libssl-dev

RUN pip install -r requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "/app/get_url_data.py"]
# EXPOSE 3333
# FROM golang:1.18beta2-alpine3.14 AS builder
# RUN apk add --no-cache git
# WORKDIR /go/src/app
# COPY . .
# RUN go get -d -v ./...
# RUN go build -o /go/bin/app -v ./...
# ENTRYPOINT ["./app"]


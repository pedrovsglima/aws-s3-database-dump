FROM ubuntu:focal

RUN apt-get update && apt-get install -y mysql-client

ENV TZ=America/Sao_Paulo

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    apt-get update && apt-get install -y tzdata && dpkg-reconfigure -f noninteractive tzdata

CMD tail -f /dev/null

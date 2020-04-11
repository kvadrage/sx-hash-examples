# sx_lag_hash container

FROM ubuntu:bionic
RUN apt update && apt --no-install-recommends -y install python

WORKDIR /
COPY ./sx_lag_hash.py /usr/bin/
COPY ./sx_lag_hash.json /etc/sx_hash/
CMD ["python", "/usr/bin/sx_lag_hash.py"]

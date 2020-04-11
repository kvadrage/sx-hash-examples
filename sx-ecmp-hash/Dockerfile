# sx_ecmp_hash container

FROM ubuntu:bionic
RUN apt update && apt --no-install-recommends -y install python

WORKDIR /
COPY ./sx_ecmp_hash.py /usr/bin/
COPY ./sx_ecmp_hash.json /etc/sx_hash/
CMD ["python", "/usr/bin/sx_ecmp_hash.py"]

#!/bin/bash
VERSION=$1

if [ -z "$VERSION" ]
then
	echo "Usage: $0 <VERSION>"
	exit 1
fi

docker build -t "sx-lag-hash:$VERSION" .
docker save -o sx_lag_hash_$VERSION.tar.gz sx-lag-hash:$VERSION
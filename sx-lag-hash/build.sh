#!/bin/bash
VERSION=$1

if [ -z "$VERSION" ]
then
	echo "Usage: $0 <VERSION>"
	exit 1
fi

docker build -t "sdk-lag-hash:$VERSION" .
docker save -o sdk_lag_hash_$VERSION.tar.gz sdk-lag-hash:$VERSION
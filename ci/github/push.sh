#!/bin/bash
set -x

docker tag ${NAME_APP}:${VERSION} ghcr.io/${OWNER}/${NAME_APP}:${VERSION}
docker push ghcr.io/${OWNER}/${NAME_APP}:${VERSION}
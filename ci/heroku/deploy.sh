#!/bin/bash
#set -x

docker tag ${NAME_APP}:${VERSION} registry.heroku.com/${NAME_APP}/web:${VERSION}
IMAGE_ID=$(docker inspect --format="{{.Id}}" registry.heroku.com/${NAME_APP}/web)
docker push registry.heroku.com/${NAME_APP}/web:${VERSION}

curl --netrc -X PATCH https://api.heroku.com/apps/${NAME_APP}/formation \
  -d '{
  "updates": [
    {
      "type": "web",
      "docker_image": "'${IMAGE_ID}'"
    }
  ]
}' \
  -H "Content-Type: application/json" \
  -H "Accept: application/vnd.heroku+json; version=3.docker-releases"\
  -H "Authorization: Bearer ${HEROKU_TOKEN}"


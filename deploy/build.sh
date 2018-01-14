#!/bin/bash

host=192.168.0.11
# host=localhost

echo "Building images"
docker build -q -t skivrige/nginx nginx
docker build -q -t skivrige/scraper ../scraper
docker build -q -t skivrige/backend ../backend
docker build -q -t skivrige/frontend ../frontend

echo "Tagging images"
docker tag skivrige/nginx $host:5000/skivrige/nginx
docker tag skivrige/scraper $host:5000/skivrige/scraper
docker tag skivrige/backend $host:5000/skivrige/backend
docker tag skivrige/frontend $host:5000/skivrige/frontend

echo "Pushing images"
docker push $host:5000/skivrige/nginx
docker push $host:5000/skivrige/scraper
docker push $host:5000/skivrige/backend
docker push $host:5000/skivrige/frontend
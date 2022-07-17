#!/bin/bash
docker run --rm -it \
  -w /project \
  -p 8081:8081 \
  --volume $PWD:/project \
  --user $(id -u):$(id -g) \
  node:16.15-alpine /bin/sh

#!/bin/sh
docker run -d -p 8000:8080 -v $(pwd)/tests/wiremock/__files:/home/wiremock/__files -v $(pwd)/tests/wiremock/mappings:/home/wiremock/mappings --name=redcoffee-test-wiremock-container wiremock/wiremock:latest
sleep 10
docker ps

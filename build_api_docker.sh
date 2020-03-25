#!/bin/bash

pipenv lock --requirements > requirements.txt
docker build -t ncov19 -f Dockerfile .
#!/bin/bash 
sudo docker-compose -f docker-compose.yaml -f inventory/docker-compose.yaml -f users/docker-compose.yaml -f auth/docker-compose.yaml up
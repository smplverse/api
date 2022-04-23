#!/bin/bash

# usage:
# sudo ./obtain-cert.sh <domain> <email>

sudo cp -R ./nginx /etc/

sudo apt-get update && sudo apt-get install -y \
  certbot \
  python3-certbot-nginx

sudo cerbot --nginx -d $1 -m $2 --agree-tos

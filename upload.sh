#!/bin/sh
curl -X POST --data-binary "@${1}" -H'Content-Type: application/octet-stream' localhost:5000/upload
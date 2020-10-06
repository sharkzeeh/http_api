#!/bin/sh
gunicorn -w 1 -b 0:5000 flask_app:app --daemon
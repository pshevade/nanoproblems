#!/bin/bash

if [ $1 == "--local" ]; then
    export LOCAL=True
    export DB_URI='my_uri'
fi

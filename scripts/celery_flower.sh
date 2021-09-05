#!/bin/bash
source env.sh
celery flower -A app.worker
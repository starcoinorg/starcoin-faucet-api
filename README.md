# 

## 1. install
```shell
pip install -r requirement.txt
```

starcoin-sdk init
```shell
cd starcoin-sdk-python
python setup.py install
```

twint with the local code, source of pip doesn't work


## 2. Config

env
```shell
export PATH=$PATH:`python local bin`
export PYTHONPATH=`project path`
#

# 1. config : mysql、redis etc
copy scripts/env.sh.test scripts/env.sh

# 2. source （ must run ）
source ./scripts/env.sh
```


## 3. db migrate
```shell
# generate migration config file
alembic revision --autogenerate
# migrate
alembic upgrade head
```

## 4. runserver
```shell
# root
uvicorn app.main:app --reload --host 0.0.0.0 
# run
cd scripts && ./celery_worker.sh
# monitor
cd scripts && ./celery_flower.sh
```

# links
swagger api： http://localhost:8000/docs
celery flower: http://127.0.0.1:5555/

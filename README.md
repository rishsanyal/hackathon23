# Docker Flask Celery Redis

A basic [Docker Compose](https://docs.docker.com/compose/) template for orchestrating a [Flask](http://flask.pocoo.org/) application & a [Celery](http://www.celeryproject.org/) queue with [Redis](https://redis.io/)

### Installation

```bash
git clone https://github.com/mattkohl/docker-flask-celery-redis
```

### Build & Launch

```bash
docker-compose up -d --build
```

### Enable hot code reload

```
docker-compose -f docker-compose.yml -f docker-compose.development.yml up --build
or
sudo -E docker-compose -f docker-compose.development.yml up  --build
```

This will expose the Flask application's endpoints on port `5001` as well as a [Flower](https://github.com/mher/flower) server for monitoring workers on port `5555`

To add more workers:
```bash
docker-compose up -d --scale worker=5 --no-recreate
```

To shut down:

```bash
docker-compose down
```

To interact with the backend using shell:
```bash
docker-compose exec web flask shell
```

    This probably needs some work like auto-complete, auto-importing of models, etc.


App Specifics:
- To change the endpoints, update the code in [api/app.py](api/app.py)
- Task changes should happen in [celery-queue/tasks.py](celery-queue/tasks.py)
- To add new models, update [api/models.py](api/models.py)

- Default User Auth: user1/user1234



---

adapted from [https://github.com/itsrifat/flask-celery-docker-scale](https://github.com/itsrifat/flask-celery-docker-scale)





------------------------------------

Progress:
6/19
- Don't think we need to remove a user from the queue just yet when they close the window. In the future we'd add that functionality of the user getting kicked out of the queue once the window's closed.


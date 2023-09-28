# FLASK REST API

This demo project was created using python, Flask, SQLAlchemy ORM, Redis, PostgreSQL and Docker. It consists of a simple rest api of a blog, with user authentication, articles, images upload and likes feature. The project itself allows the usual CRUD operations.

The project uses Redis RQ. A second instance of the project must be started with the command: rq worker -u redis://url tasks in order to process the jobs that are placed in the queue.

During the development, all services on which the project depends were created using docker-compsose.

```
version: '3.8'

services:
  app:
    build: ../.
    depends_on:
      - db
      - redis

  worker:
    build: ../.

    command: ['rq', 'worker', '-u', 'redis://redis', 'tasks']
    env_file:
      - ../.env
    depends_on:
      - redis

  db:
    image: postgres:14.3
    restart: unless-stopped
    volumes:
      - postgres-data:/var/lib/postgresql/data
    env_file:
      - ./config/postgresql.env

  pgadmin:
    container_name: pgadmin4_container
    image: dpage/pgadmin4
    restart: unless-stopped
    volumes:
      - pgadmin-data:/var/lib/pgadmin
    env_file:
      - ./config/pgadmin.env
    ports:
      - '8080:8080'

  redis:
    image: redis:latest
    command: ['redis-server', '--appendonly', 'yes']
    volumes:
      - redis-data:/data

  rq-dashboard:
    image: cjlapao/rq-dashboard:latest
    ports:
      - '9181:9181'
    env_file:
      - ./config/rd-dashboard.env
    depends_on:
      - redis

volumes:
  postgres-data:
  pgadmin-data:
  redis-data:


```

## 🔧 Runing the project

### ENV FILE

Provide a .env file on the root level of the project with the following variables:

#### Flask

- FLASK_ENV=development - example
- BASE_URL=http://127.0.0.1:5000 - example
- ENV=dev or prod

#### JWT

- JWT_SECRET_KEY=some_long_secret_hash_like_string
- JWT_EXPIRATION_MINUTES=50

#### Database

- DATABASE_DEV_URL=postgresql://........ or sqlite
- DATABASE_TEST_URL=sqlite://:memory:
- DATABASE_PROD_URL=PROD_URL

#### Redis

- REDIS_URL=redis//.......

#### Email

- EMAIL_API_URL=https://api.mailgun.net/v3
- EMAIL_API_KEY=email_service_key
- EMAIL_DOMAIN=ssomedomain.com

<p align="center">Copyright © 2023 João Aroeira</p>

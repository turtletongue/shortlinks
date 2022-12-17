# Getting started

You can use docker-compose to easily start app.

First of all, install [docker-compose](https://docs.docker.com/compose/install/) if you don't have it on your machine. Make sure you follow all prerequisites.

Secondly, you should create .env file with following content (example):

```
# Base URL for redirects
SITE_URL=http://localhost:3030/

# Secret key for auth cookies
SECRET_KEY=super_secret

# PostgreSQL database user
POSTGRES_USER=your_user

# PostgreSQL database password
POSTGRES_PASSWORD=your_password

# PostgreSQL database name
POSTGRES_DB=your_db

# Connection string for database operations
DB_CONNECTION="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@shortlinks-db/${POSTGRES_DB}"

MIN_PASSWORD_LENGTH=7

# Minimum link UUID length (only affects the part after the base URL)
LINK_LENGTH=8
```

Now, you can start the project:

```
docker-compose up
```
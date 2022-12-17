# Getting started

You can use docker-compose to easily start app.

First of all, install [docker-compose](https://docs.docker.com/compose/install/) if you don't have it on your machine. Make sure you follow all prerequisites.

Second, create `.database.env` file and fill it with your postgres database variables. For example:

```
POSTGRES_USER=your_user

POSTGRES_PASSWORD=your_password

POSGRES_DB=your_db
```

Third, you should create .env file with following content (example):

```
# Base URL for redirects
SITE_URL=http://localhost:3030/

# Secret key for auth cookies
SECRET_KEY=super_secret

# Connection string for database operations
DB_CONNECTION="postgresql://your_user:your_password@shortlinks-db/your_db"

MIN_PASSWORD_LENGTH=7

# Minimum link UUID length (only affects the part after the base URL)
LINK_LENGTH=8
```

Now, you can start the project:

```
docker-compose up
```
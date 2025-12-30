# Stage 2:

In this stage, we will configure a database.

We will use the official PostgreSQL image:

- [https://hub.docker.com/_/postgres](https://hub.docker.com/_/postgres)

## Objectives

Required database configuration:

- Create a Postgres container with the name `hyper-postgres`;
- Define environment variables for the Postgres password, user and database name;
- Bind host port `5432` to container port `5432`;
- For container network use `hyper-network`;
- For container volume use `hyper-volume` and map it to `/var/lib/postgresql/data`;
- Run the container in detached mode;
- Use the official `postgres` image with the tag `15.3`.

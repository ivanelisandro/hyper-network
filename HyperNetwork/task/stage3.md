# Stage 3:

In this stage, we will create a container to manage the database.

We will use  a database management tool called `adminer`.

The official `adminer` image can be found here:

- [https://hub.docker.com/_/adminer](https://hub.docker.com/_/adminer)

## Objectives

Required configuration:

- Create an `adminer` container with the name `hyper-adminer`;
- Bind the host port `8080` to container port `8080`;
- For container network use `hyper-network`;
- Run the container in `detached` mode;
- Use the official `adminer` image with the tag `4.8.1`.

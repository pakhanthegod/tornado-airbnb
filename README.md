# Tornado airbnb project

## Navigation

- [Tornado airbnb project](#tornado-airbnb-project)
  - [Navigation](#navigation)
- [Tests](#tests)
- [Liquibase](#liquibase)
  - [Migrate](#migrate)
  - [Clear check sums](#clear-check-sums)

# Tests

To run tests you need to execute a code below:

>`$ docker-compose run --rm app pytest tests`

# Liquibase

To use liquibase commands you need to execute that code below :

>`$ docker-compose run --rm migrate liquibase --username=${PSQL_USER} --password=${PSQL_PASSWORD} [command]`

`PSQL_USER` and `PSQL_PASSWORD` are database access variables from `.env` file that contains your environment variables.

## Migrate

To apply initial migrates to the database execute this command:

> `$ docker-compose run --rm migrate liquibase --username=${PSQL_USER} --password=${PSQL_PASSWORD} migrate`

## Clear check sums

If you have changed migration files and get error about check sums after execution `migrate` command run this:

> `$ docker-compose run --rm migrate liquibase --username=${PSQL_USER} --password=${PSQL_PASSWORD} clearCheckSums`

# dummy
> this application was generated using [Django Ninja REST API Generator](https://github.com/roymanigley/django-ninja-restapi-generator)

## Requirements

- Python3
- venv
- docker-compose

## Initial build

### Local
> creates a default user `admin` with the password `admin`, the database is a postgresql in docker-compose which is automaticly started when the script is executed

    ./build_local.sh

### Prod 
> creates a default user according to the environment variables, some environment variables are requires, just take a look at `./build_prod.sh`

    ./build_prod.sh
    
## Run the application

### Local
> starts the application with DEBUG=True

    ./run_local.sh

### Prod
> starts the application with DEBUG=False, some environment variables are requires, just take a look at `./run_prod.sh`

    ./run_prod.sh

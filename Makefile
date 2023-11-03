include .env

help:
	@echo "## docker-build			- Build Docker Images (amd64) including its inter-container network."
	@echo "## docker-build-arm		- Build Docker Images (arm64) including its inter-container network."
	@echo "## postgres			- Run a Postgres container  "
	@echo "## spark			- Run a Spark cluster, rebuild the postgres container, then create the destination tables "
	@echo "## jupyter			- Spinup jupyter notebook for testing and validation purposes."
	@echo "## airflow			- Spinup airflow scheduler and webserver."
	@echo "## kafka			- Spinup kafka cluster (Kafka+Zookeeper)."
	@echo "## clean			- Cleanup all running containers related to the challenge."

docker-build:
	@echo '__________________________________________________________'
	@echo 'Building Docker Images ...'
	@echo '__________________________________________________________'
	@docker network inspect dataeng-network >/dev/null 2>&1 || docker network create dataeng-network
	@echo '__________________________________________________________'
	@docker build -t dataeng-dibimbing/airflow -f ./docker/Dockerfile.airflow .
	@echo '__________________________________________________________'
	@docker build -t dataeng-dibimbing/jupyter -f ./docker/Dockerfile.jupyter .
	@echo '==========================================================='

docker-build-arm:
	@echo '__________________________________________________________'
	@echo 'Building Docker Images ...'
	@echo '__________________________________________________________'
	@docker network inspect dataeng-network >/dev/null 2>&1 || docker network create dataeng-network
	@echo '__________________________________________________________'
	@docker build -t dataeng-dibimbing/spark -f ./docker/Dockerfile.spark .
	@echo '__________________________________________________________'
	@docker build -t dataeng-dibimbing/airflow -f ./docker/Dockerfile.airflow-arm .
	@echo '__________________________________________________________'
	@docker build -t dataeng-dibimbing/jupyter -f ./docker/Dockerfile.jupyter .
	@echo '==========================================================='

jupyter:
	@echo '__________________________________________________________'
	@echo 'Creating Jupyter Notebook Cluster at http://localhost:${JUPYTER_PORT} ...'
	@echo '__________________________________________________________'
	@docker-compose -f ./docker/docker-compose-jupyter.yml --env-file .env up -d
	@echo 'Created...'
	@echo 'Processing token...'
	@sleep 20
	@docker logs ${JUPYTER_CONTAINER_NAME} 2>&1 | grep '\?token\=' -m 1 | cut -d '=' -f2
	@echo '==========================================================='


airflow:
	@echo '__________________________________________________________'
	@echo 'Creating Airflow Instance ...'
	@echo '__________________________________________________________'
	@docker-compose -f ./docker/docker-compose-airflow.yml --env-file .env up
	@echo '==========================================================='

postgres: postgres-create postgres-create-table postgres-ingest-csv

postgres-create:
	@docker-compose -f ./docker/docker-compose-postgres.yml --env-file .env up -d
	@echo '__________________________________________________________'
	@echo 'Postgres container created at port ${POSTGRES_PORT}...'
	@echo '__________________________________________________________'
	@echo 'Postgres Docker Host	: ${POSTGRES_CONTAINER_NAME}' &&\
		echo 'Postgres Account	: ${POSTGRES_USER}' &&\
		echo 'Postgres password	: ${POSTGRES_PASSWORD}' &&\
		echo 'Postgres Db		: ${POSTGRES_DB}'
	@sleep 5
	@echo '==========================================================='

postgres-create-table:
	@echo '__________________________________________________________'
	@echo 'Creating tables fact_kabko...'
	@echo '_________________________________________'
	@docker exec -it ${POSTGRES_CONTAINER_NAME} psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -f sql/ddl-lat-long.sql
	@echo '==========================================================='
	@echo '__________________________________________________________'
	@echo 'Creating tables dim_weather...'
	@echo '_________________________________________'
	@docker exec -it ${POSTGRES_CONTAINER_NAME} psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -f sql/ddl-weather.sql
	@echo '==========================================================='
	@echo '__________________________________________________________'
	@echo 'Creating tables dim_air_quality...'
	@echo '_________________________________________'
	@docker exec -it ${POSTGRES_CONTAINER_NAME} psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -f sql/ddl-air-quality.sql
	@echo '==========================================================='

postgres-ingest-csv:
	@echo '__________________________________________________________'
	@echo 'Ingesting CSV...'
	@echo '_________________________________________'
	@docker exec -it ${POSTGRES_CONTAINER_NAME} psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -f sql/ingest-lat-long.sql
	@echo '==========================================================='


clean:
	@bash ./scripts/goodnight.sh
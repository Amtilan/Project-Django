DC = docker compose
STORAGES_FILE = docker_compose\storages.yaml
EXEC = docker exec -it
DB_CONTAINER = postgres_db
ENV = --env-file .env
LOGS = docker logs

.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV} up -d

.PHONY: storages-logs
storages-logs:
	${LOGS} ${DB_CONTAINER} -f

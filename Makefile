DC = docker compose
STORAGES_FILE = docker_compose\storages.yaml
EXEC = docker exec -it
DB_CONTAINER = postgres_db
ENV = --env-file .env
LOGS = docker logs
MANAGE_FILE = python manage.py
APP_FILE = docker_compose\app.yaml
APP_CONTAINER = main-app

#Для того чтобы создать в докере psql
.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV} up -d

# Для того чтобы выключить/удалить БД(всё ещё не разобрался)
.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} down

# Для того чтобы смотреть логи БД
.PHONY: storages-logs
storages-logs:
	${LOGS} ${DB_CONTAINER} -f

.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} -f ${STORAGES_FILE} ${ENV} up --build -d

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} down

.PHONY: migrate
migrate:
	${EXEC} ${APP_CONTAINER} ${MANAGE_FILE} migrate

.PHONY: migrations
migrations:
	${EXEC} ${APP_CONTAINER} ${MANAGE_FILE} makemigrations

.PHONY: superuser
superuser:
	${EXEC} ${APP_CONTAINER} ${MANAGE_FILE} createsuperuser

.PHONY: collect-static
collect-static:
	${EXEC} ${APP_CONTAINER} ${MANAGE_FILE} collectstatic

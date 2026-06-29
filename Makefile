# Имя проекта (можно поменять)
PROJECT_NAME=user_microservice

# Сервисы
APP_SERVICE=app
DB_SERVICE=db

# ======================
# Основные команды
# ======================

# Сборка контейнеров
build:
	docker-compose build

# Запуск контейнеров (в фоне)
up:
	docker-compose up -d

# Остановка контейнеров
down:
	docker-compose down

# Перезапуск контейнеров
restart: down up

# ======================
# Работа с сервисами
# ======================

# Войти в контейнер приложения
app-shell:
	docker-compose exec $(APP_SERVICE) bash

# Войти в контейнер базы данных (psql)
db-shell:
	docker-compose exec $(DB_SERVICE) bash

# Подключиться к Postgres через psql
db-psql:
	docker-compose exec $(DB_SERVICE) psql -U $$DB_USER -d $$DB_NAME

# ======================
# Очистка
# ======================

# Остановить и удалить контейнеры + тома
clean:
	docker-compose down -v

# Полная очистка (включая образы)
prune:
	docker-compose down -v --rmi all --remove-orphans

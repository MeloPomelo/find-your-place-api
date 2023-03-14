# find-your-place-api
This is a project template which uses [FastAPI](https://fastapi.tiangolo.com/), [Alembic](https://alembic.sqlalchemy.org/en/latest/) and async [SQLModel](https://sqlmodel.tiangolo.com/) as ORM. It shows a complete async CRUD template using authentication.

## Настройка среды
Создать **.env** файл в корневой папке проекта. Содержимое скопируйте из **.env.example**. Изменить в соответствии с вашей конфигурацией.

## Запускаем проект с использованием Docker и настройкой контейнеров
### Docker compose commands
*создание контейнеров и подключение всех библиотек*
```sh
docker-compose build
```
*миграция базы данных*
```sh
docker-compose run fastapi_server alembic revision --autogenerate -m "mig"
```
```sh
docker-compose run fastapi_server alembic upgrade head
```
*создание супер юзера*
```sh
docker-compose run fastapi_server python app/init_data.py
```
*запуск контейнеров*
```sh
docker-compose up
```
### Docker commands
*Очистка контейнеров*
```sh
docker system prune -a
```

## URLS
- *fastapi swagger* [http://fastapi.localhost/docs](http://fastapi.localhost/docs)
- *pgadmin* [http://localhost:5050](http://localhost:5050)
- *minio* [http://storage.localhost](http://storage.localhost)
- *traefik* [http://traefik.localhost](http://traefik.localhost)

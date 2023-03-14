# find-your-place-api
This is a project template which uses [FastAPI](https://fastapi.tiangolo.com/), [Alembic](https://alembic.sqlalchemy.org/en/latest/) and async [SQLModel](https://sqlmodel.tiangolo.com/) as ORM. It shows a complete async CRUD template using authentication.

## Настройка среды
Создать **.env** файл в корневой папке проекта. Содержимое скопируйте из **.env.example**. Изменить в соответствии с вашей конфигурации.

## Запускаем проект с использованием Docker и настройкой контейнеров
#Docker compose commands
*создание контейнеров и подключение всех библиотек*
```sh
docker-compose build
```
*миграция базы данных*
```docker-compose run fastapi_server alembic revision --autogenerate -m "mig"```
```docker-compose run fastapi_server alembic upgrade head```
*создание супер юзера*
```docker-compose run fastapi_server python app/init_data.py```
*запуск контейнеров*
```docker-compose up```
## Команды для docker
*Очистка контейнеров*
```docker system prune -a```

## URLS
*FAST_API SWAGGER* [http://fastapi.localhost/docs](http://fastapi.localhost/docs)
*pgadmin* [http://localhost:5050](http://localhost:5050)
*minio* [http://storage.localhost](http://storage.localhost)
*traefik* [http://traefik.localhost](http://traefik.localhost)
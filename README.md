# Car-Service
Сервис предоставляет агрегированные данные по услугам компаний в сфере автомобильных услуг, включая техническое обслуживание, ремонт, страхование и другие. Пользователи могут:

- записываться на услуги онлайн
- оставлять заявки на услуги
- искать компании и услуги на карте
- оставлять отзывы и оценки компаний и услуг

[Frontend](https://car-service-18635.web.app/)

[Backend api](https://gas159.ru/docs#/)

### Стек (backend)
FastApi, SQLalchemyORM, Redis, postgres, docker-compose, alembic, pydantic, i118n.
## Installation


установить python 3.12e

в терминале установить менеджер зависимостей poetrey

```
$ pip install poetry 
```
```
$ git clone https://github.com/Gas159/Car-Service.git
```
перейти в папку с проектом:
```
$ cd Car_Service
```

далее все выполнять в виртульном окружении. make shell создаст его если нету.
```
$ make shell 
```

установить все зависимости
```
$ make install 
```

запустить файл server/main.py

открыть бразер по адресу:
http://0.0.0.0:8000/ 
#docker comand 45.9.73.213
build:
		docker build . --tag my1

drun:
		docker run -d --name fastapi -p 8001:8000 my

stop:
		@if [ -n "$$(docker ps -q)" ]; then docker stop $$(docker ps -q); fi

rm:
		@if [ -n "$$(docker ps -aq)" ]; then docker rm $$(docker ps -aq); fi

rmi:
		@if [ -n "$$(docker images -q)" ]; then docker rmi -f $$(docker images -q); fi

prune:
		docker system prune -a

clean: stop rm rmi


reload:
		docker-compose stop && docker-compose up --build

redown: #Удалит тома и контейнер
		docker-compose down  && docker-compose up --build app pg adminer



run:
		gunicorn main:main_app --workers 3 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8003 --reload

run1:
		uvicorn main:main_app --host 0.0.0.0 --port 443 --ssl-keyfile /etc/letsencrypt/live/gas159.ru/privkey.pem --ssl-certfile /etc/letsencrypt/live/gas159.ru/fullchain.pem --reload

run2:
		uvicorn main:main_app --host 0.0.0.0 --port 443 --ssl-keyfile /etc/letsencrypt/live/gas159.ru/privkey.pem --ssl-certfile /etc/letsencrypt/live/gas159.ru/fullchain.pem --workers 3

run3:
		uvicorn main:main_app --host 0.0.0.0 --port 8001  --reload


tmux:
		tmux attach -t fast

celery:
		celery -A project_services.task_celery.tasks:celery worker -l info


#poetry
shell:
		poetry shell

tree:
		poetry show --tree

install:
		poetry install

install_depends:
		poetry export -f requirements.txt --output requirements.txt --without-hashes --only main # экпорт зависимостей
		poetry self add poetry-plugin-export
		pip3 freeze > requirements.txt
		pip  install -r requirements.txt

		poetry export -f requirements.txt > requirements.txt
		python -m pip install -r requirements.txt
		poetry install


# alembic
revision:
		alembic revision --autogenerate
		45.9.73.213


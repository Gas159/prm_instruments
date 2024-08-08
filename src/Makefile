#docker comand
build:
		docker build . --tag my1
# run:
# 		docker run -d --name fastapi -p 8001:8000 my

run:
		gunicorn main:main_app --workers 3 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001 --reload
tmux:
		tmux attach -t fast


#poetry
shell:
		poetry shell

tree:
		poetry show --tree

install:
		poetry install

install_depends:
		poetry export -f requirements.txt > requirements.txt
		python -m pip install -r requirements.txt
		poetry install

# alembic
revision:
		alembic revision --autogenerate


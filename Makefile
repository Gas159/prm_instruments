build:
        docker build . --tag my1
run:
        docker run -p 8001:8000 
tree:
	poetry show --tree

install:
	poetry install

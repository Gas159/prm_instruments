build:
        docker build . --tag my1

run:
        docker run -p 8001:8000

tree:
        poetry show --tree

install:
        poetry install

install_depends:
        poetry export -f requirements.txt > requirements.txt
        python -m pip install -r requirements.txt
        poetry install


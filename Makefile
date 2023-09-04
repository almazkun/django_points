FILES = .

REGISTRY=ghcr.io/almazkun
IMAGE_NAME=django-points
CONTAINER_NAME=django-points-container
VERSION=0.1.0

build:
	docker build -t $(REGISTRY)/$(IMAGE_NAME):$(VERSION) .
	docker tag $(REGISTRY)/$(IMAGE_NAME):$(VERSION) $(REGISTRY)/$(IMAGE_NAME):latest

push:
	docker push $(REGISTRY)/$(IMAGE_NAME):$(VERSION)
	docker push $(REGISTRY)/$(IMAGE_NAME):latest

pull:
	docker pull $(REGISTRY)/$(IMAGE_NAME):latest

run:
	docker run -it --rm --name $(CONTAINER_NAME) -p 8000:8000 $(REGISTRY)/$(IMAGE_NAME):$(VERSION)

migrate:
	docker exec -it $(CONTAINER_NAME) python manage.py migrate


lint:
	pipenv run isort --force-single-line-imports --line-width 999 ${FILES}
	pipenv run autoflake --ignore-init-module-imports --in-place --remove-all-unused-imports ${FILES}
	pipenv run isort --use-parentheses --trailing-comma --multi-line 3 --force-grid-wrap 0 --line-width 140 ${FILES}
	pipenv run black ${FILES}
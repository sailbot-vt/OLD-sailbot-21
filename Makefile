# Builds the base, development, production, and testing images to local docker daemon
.PHONY: build
build:
	docker build -t sailbotvt/sailbot-20:beaglebone-black-debian-stretch-python -f Dockerfile.base .
	docker build -t sailbotvt/sailbot-20:sailbot-development -f Dockerfile.dev .
	docker build -t sailbotvt/sailbot-20:sailbot-test -f Dockerfile.test .
	docker build -t sailbotvt/sailbot-20:sailbot-production -f Dockerfile.prod .

.PHONY: build_base
build_base:
	docker build -t sailbotvt/sailbot-20:beaglebone-black-debian-stretch-python -f Dockerfile.base .

.PHONY: build_dev
build_dev:
	docker build -t sailbotvt/sailbot-20:sailbot-development -f Dockerfile.dev .

.PHONY: build_test
build_test:
	docker build -t sailbotvt/sailbot-20:sailbot-test -f Dockerfile.test .

.PHONY: build_prod
build_prod:
	docker build -t sailbotvt/sailbot-20:sailbot-production -f Dockerfile.prod .

# Builds a local beaglebone base and production image, 
# and the beaglebone-img.tar.gz to be loaded onto the beaglebone through scp.
# Note: Requires `experimental = True` in docker-daemon config file
.PHONY: build_prod_tar
build_prod_tar:
	docker build -t sailbotvt/sailbot-20:beaglebone-black-debian-stretch-python -f Dockerfile.base . --squash
	docker build -t sailbotvt/sailbot-20:sailbot-production -f Dockerfile.prod . --squash
	docker save -o beaglebone-img.tar.gz sailbotvt/sailbot-20:sailbot-production
	echo "Copy over to beaglebone using rsync, scp, ... \n Then load on beaglebone using: \n docker load -i <path_to_tar_file>"

# Starts bash in the development image.
.PHONY: dev
dev:
	docker build -t sailbotvt/sailbot-20:sailbot-development -f Dockerfile.dev .
	docker run -it --rm --name sailbot_dev sailbotvt/sailbot-20:sailbot-development bash

# Run tests on a production-ready image.
.PHONY: test
test:
	docker build -t sailbotvt/sailbot-20:sailbot-test -f Dockerfile.test .
	docker run -it --rm --name sailbot_test sailbotvt/sailbot-20:sailbot-test ./scripts/test.sh

# Runs main.py on the production image.
.PHONY: run
run:
	docker run -it --rm --privileged --name sailbot_run sailbotvt/sailbot-20:sailbot-production ./scripts/run.sh

# Connects to bash on the production image.
.PHONY: run_cli
run_cli:
	docker run -it --rm --privileged --name sailbot_run sailbotvt/sailbot-20:sailbot-production bash

# Removes docker images and containers.
.PHONY: clean_docker
clean:
	docker image prune -a

# Cleans the sailbot directory
.PHONY: clean
clean:
	rm logs/*

# These don't work? 
.PHONY: test_tracker
test_tracker:
	bash ./scripts/test_tracker.sh

.PHONY: test_controls
test_controls:
	bash ./scripts/test_controls.sh

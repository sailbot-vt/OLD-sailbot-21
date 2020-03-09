# Builds the base development image
.PHONY: build_dev_base
build_dev_base:
	docker build -t sailbotvt/sailbot-20:sailbot-development-base --build-arg FLAVOR=stretch -f Dockerfile.base_dev .

# Warning: build_base takes a *VERY* long time to compile (>7 hours).
# > Unless you've updated Dockerfile.base, never do this to yourself.
# > Docker will load the latest base image from Dockerhub when needed.
.PHONY: build_base
build_base:
	docker build -t sailbotvt/sailbot-20:beaglebone-black-debian-stretch-python -f Dockerfile.base .

# Builds a local beaglebone production image, 
# and the beaglebone-img.tar.gz to be loaded onto the beaglebone through scp.
# Note: Requires `experimental = True` in docker-daemon config file
# 		as well as the latest beaglebone image in sailbot's dockerhub
.PHONY: build_prod_tar
build_prod_tar:
	# docker build -t sailbotvt/sailbot-20:beaglebone-black-debian-stretch-python -f Dockerfile.base . --squash
	docker build -t sailbotvt/sailbot-20:sailbot-production -f Dockerfile.prod . --squash
	docker save -o beaglebone-img.tar.gz sailbotvt/sailbot-20:sailbot-production
	echo "Copy over to beaglebone using rsync, scp, ... \n Then load on beaglebone using: \n docker load -i <path_to_tar_file>"

# Starts bash in the development image.
.PHONY: dev
dev:
	docker build -t sailbotvt/sailbot-20:sailbot-development -f Dockerfile.dev .
	docker run -it --rm --name sailbot_dev sailbotvt/sailbot-20:sailbot-development bash

# Runs tests on development image.
.PHONY: test_dev
test_dev:
	docker build -t sailbotvt/sailbot-20:sailbot-dev-test -f Dockerfile.dev .
	docker run -it --rm --name sailbot_dev_test sailbotvt/sailbot-20:sailbot-dev-test ./scripts/test.sh -e TRAVIS_JOB_ID="$TRAVIS_JOB_ID" -e TRAVIS_BRANCH="$TRAVIS_BRANCH"

# Run tests on a production-ready image.
.PHONY: test
test:
	docker build -t sailbotvt/sailbot-20:sailbot-test -f Dockerfile.test .
	docker run -it --rm --name sailbot_test sailbotvt/sailbot-20:sailbot-test ./scripts/test.sh -e TRAVIS_JOB_ID="$TRAVIS_JOB_ID" -e TRAVIS_BRANCH="$TRAVIS_BRANCH"

# Runs main.py on the production image.
.PHONY: run
run:
	docker build -t sailbotvt/sailbot-20:sailbot-production -f Dockerfile.prod .
	docker run -it --rm --privileged --name sailbot_run sailbotvt/sailbot-20:sailbot-production ./scripts/run.sh

# Connects to bash on the production image.
.PHONY: run_cli
run_cli:
	docker build -t sailbotvt/sailbot-20:sailbot-production -f Dockerfile.prod .
	docker run -it --rm --privileged --name sailbot_run sailbotvt/sailbot-20:sailbot-production bash

# Removes docker images and containers.
.PHONY: clean_docker
clean_docker:
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

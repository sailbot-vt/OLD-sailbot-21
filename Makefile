_init:
	bash ./scripts/init.sh

test:
	docker build -t sailbotvt/sailbot-20:deployment_testing_dev -f Dockerfile.dev .
	docker run -it --rm --name sailbotvt/sailbot-20:deployment_testing_dev ./scripts/test.sh

test_production:
	docker build -t sailbotvt/sailbot-20:deployment_testing_beaglebone -f Dockerfile.prod .
	docker run -it --rm --privileged --name sailbot_run sailbotvt/sailbot-20:deployment_testing_beaglebone ./scripts/test.sh

run:
	docker run -it --rm --privileged --name sailbot_run sailbotvt/sailbot-20:deployment_testing_beaglebone ./scripts/run.sh

run_cli:
	docker run -it --rm --privileged --name sailbot_run sailbotvt/sailbot-20:deployment_testing_beaglebone bash

build_prod:
	docker build -t sailbotvt/sailbot-20:deployment_testing_beaglebone -f Dockerfile.prod .
	docker save -o beag_img.tar.gz sailbotvt/sailbot-20:deployment_testing_beaglebone
	echo "Copy over to beaglbone using rsync, scp, ... \n Then load on beaglbeone using: \n docker load -i <path_to_tar_file>"

clean:
	rm logs/*

test_tracker:
	bash ./scripts/test_tracker.sh

test_controls:
	bash ./scripts/test_controls.sh

.PHONY: _init test test_production run run_cli build_prod clean test_tracker test_controls

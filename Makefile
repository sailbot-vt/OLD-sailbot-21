_init:
	bash ./scripts/init.sh

test:
	docker build -t sailbotvt/sailbot-20:deployment_testing_dev -f Dockerfile.dev .
	docker run -it --rm --name sailbot_testing sailbotvt/sailbot-20:deployment_testing_dev ./scripts/test.sh

build:
	docker build -t sailbotvt/sailbot-20:deployment_testing_beaglebone -f Dockerfile.prod .

build_beag_img:
	docker save -o beag_img.tar.gz sailbotvt/sailbot-20:deployment_testing_beaglebone
	echo "Copy over to beaglbone using rsync, scp, ... \n Then load on beaglbeone using: \n docker load -i <path_to_tar_file>"

run:
	# docker run -it --rm --privileged --name sailbot_run sailbotvt/sailbot-20:deployment_testing_beaglebone ./scripts/run.sh
	docker run -it --rm --privileged --name sailbot_run sailbotvt/sailbot-20:deployment_testing_beaglebone bash
	
clean:
	rm logs/*

test_tracker:
	bash ./scripts/test_tracker.sh

test_controls:
	bash ./scripts/test_controls.sh

.PHONY: _init test build build_beag_img run clean test_tracker test_controls

init:
	bash ./scripts/init.sh

test:
	docker build -t deployment_testing_dev -f Dockerfile.dev .
	docker run -it --rm --name sailbot_testing deployment_testing_dev ./scripts/test.sh

test_remote_img:
	docker run -it --rm --name sailbot_testing sailbotvt/sailbot-20:deployment_testing_dev ./scripts/test.sh

build_beag_img:
	docker build -t beag_img -f Dockerfile.beag .
	docker save -o beag_img.tar.gz beag_img
	echo "Copy over to beaglbone using rsync, scp, ... \n Then load on beaglbeone using: \n docker load-i <path_to_tar_file>"

run_stretch_build:
	docker build -t beag_stretch_img -f Dockerfile.stretch .
	docker run -it --rm --privileged --name beag_stretch beag_stretch_img bash

run:
	docker run -it --rm --name sailbot_run sailbotvt/sailbot-20:deployment_testing_beaglebone ./scripts/run.sh

run_loc_img:
	docker run -it --rm --name sailbot_run beag_img ./scripts/run.sh

clean:
	rm logs/*

test_tracker:
	bash ./scripts/test_tracker.sh

test_controls:
	bash ./scripts/test_controls.sh

.PHONY: init test test_remote_img build_beag_img run run_loc_img run_stretch_build clean test_tracker test_controls

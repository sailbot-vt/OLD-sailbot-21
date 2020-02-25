_init:
	bash ./scripts/init.sh

test:
	docker build -t sailbotvt/sailbot-20:deployment_testing_dev -f Dockerfile.dev .
	docker run -it --rm --name sailbot_testing sailbotvt/sailbot-20:deployment_testing_dev ./scripts/test.sh

build_beag_img:
<<<<<<< HEAD
	docker build -t beag_img -f Dockerfile.prod .
=======
	docker run --rm --privileged hypriot/qemu-register
	docker build -t beag_img -f Dockerfile.beag .
>>>>>>> 6cff95a9b4eba66f6dd210b59f599de9e54729dc
	docker save -o beag_img.tar.gz beag_img
	echo "Copy over to beaglbone using rsync, scp, ... \n Then load on beaglbeone using: \n docker load-i <path_to_tar_file>"

run:
	docker run -it --rm --name sailbot_run sailbotvt/sailbot-20:deployment_testing_beaglebone ./scripts/run.sh

<<<<<<< HEAD
# Running as bash for now.
# Temporarily removed --privileged to check for build errors
run_loc_img:
	docker run -it --rm --privileged --name beaglebone_bash beag_img bash

clean:
	rm logs/*

test_tracker:
	bash ./scripts/test_tracker.sh

test_controls:
	bash ./scripts/test_controls.sh

.PHONY: init test test_remote_img build_beag_img run run_loc_img clean test_tracker test_controls
=======
.PHONY: _init test build_beag_img run
>>>>>>> 6cff95a9b4eba66f6dd210b59f599de9e54729dc

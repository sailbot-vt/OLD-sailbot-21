_init:
	bash ./scripts/init.sh

test:
	docker build -t sailbotvt/sailbot-20:deployment_testing_dev -f Dockerfile.dev .
	docker run -it --rm --name sailbot_testing sailbotvt/sailbot-20:deployment_testing_dev ./scripts/test.sh

build_beag_img:
	docker build -t beag_img -f Dockerfile.beag .
	docker save -o beag_img.tar.gz beag_img
	echo "Copy over to beaglbone using rsync, scp, ... \n Then load on beaglbeone using: \n docker load-i <path_to_tar_file>"

run:
	docker run -it --rm --name sailbot_run sailbotvt/sailbot-20:deployment_testing_beaglebone ./scripts/run.sh

.PHONY: _init test build_beag_img run

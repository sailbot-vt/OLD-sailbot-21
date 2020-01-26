init:
	bash ./scripts/init.sh

test:
	docker build -t deployment_testing_dev -f Dockerfile.dev .
	docker run -it --rm --name sailbot_testing deployment_testing_dev ./scripts/test.sh

test_remote_img:
	docker run -it --rm --name sailbot_testing sailbotvt/sailbot-20:deployment_testing_dev ./scripts/test.sh

run:
	docker run -it --rm --name sailbot_run sailbotvt/sailbot-20:deployment_testing_beaglebone ./scripts/run.sh

.PHONY: init test test_remote_img run

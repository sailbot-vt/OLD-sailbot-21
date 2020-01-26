init:
	bash ./scripts/init.sh

test:
	#bash ./scripts/test.sh
	bash docker run -it --rm --name sailbot_testing sailbotvt/sailbot-20:deployment_testing ./scripts/test.sh

run:
	bash docker run -it --rm --name sailbot_run sailbotvt/sailbot-20:deployment_testing ./scripts/run.sh

.PHONY: init dev_init test run

# Installs docker
.PHONY: init
init: 
	apt-get update && apt-get install -y apt-transport-https ca-certificates curl gnupg2 software-properties-common git
	curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
	add-apt-repository "deb [arch=armhf] https://download.docker.com/linux/debian $$(lsb_release -cs) stable"
	apt-get update && apt-get install -y docker-ce docker-ce-cli containerd.io
	groupadd docker
	usermod -aG docker ${USER}
	bash grow-partition.sh
	echo "Docker and partition setup, rebooting now..."
	reboot now

# Runs program on dockerhub image
.PHONY: run
run:
	docker run -it --rm --privileged --name sailbot_run sailbotvt/sailbot-20:sailbot-production ./scripts/run.sh

# Runs bash on dockerhub image
.PHONY: run_cli
run_cli:
	docker run -it --rm --privileged --name sailbot_run sailbotvt/sailbot-20:sailbot-production bash

# Loads local beaglebone image to docker engine
.PHONY: load
load:
	docker load -i beaglebone-img.tar.gz

# Cleans local docker images
.PHONY: clean_docker
clean_docker:
	docker image prune -a

# TODO setup pins for UART

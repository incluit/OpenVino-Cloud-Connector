docker-build:
	docker build -t zmq-cloud-connector .

docker-run:
	docker run -d -it -v ~/.aws:/root/.aws --name docker-cloud-connector --network host -t zmq-cloud-connector

docker-stop:
	docker stop docker-cloud-connector

docker-remove:
	docker rm docker-cloud-connector

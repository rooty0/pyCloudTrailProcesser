FUNCTION = CloudTrail-Watcher
REGION = us-west-2
ZIP_NAME = config-service-lambda-deployment-package.zip

.PHONY: clean deploy build

build: $(ZIP_NAME)

deps: requirements.txt Dockerfile.lambda lambda.py
	@[ -d $@ ] || mkdir $@
	cp *.py $@/

deploy: $(ZIP_NAME)
	PAGER="" aws lambda update-function-code \
		--region $(REGION) \
		--function-name $(FUNCTION) \
		--zip-file fileb://$<

$(ZIP_NAME): deps
	DOCKER_SCAN_SUGGEST=false docker build --build-arg ZIPFILE=$(ZIP_NAME) -t $(FUNCTION)-lambda:latest -f Dockerfile.lambda . && \
	ID=$$(docker create $(FUNCTION)-lambda /bin/true) && \
	docker cp $$ID:/$(ZIP_NAME) .

clean:
	rm -rf deps $(ZIP_NAME)
	docker ps -qaf "ancestor=$(FUNCTION)-lambda"| xargs docker rm && docker image rm $(FUNCTION)-lambda || exit 0

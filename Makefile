# set up the login key using the heroku cli
heroku-login:
	heroku container:login

build-ml-api-heroku: heroku-login # dependecy
	docker build --build-arg PIP_EXTRA_INDEX_URL=${PIP_EXTRA_INDEX_URL} -t registry.heroku.com/${HEROKU_APP_NAME}/web .

push-ml-api-heroku: heroku-login
	docker push registry.heroku.com/${HEROKU_APP_NAME}/web

release-ml-api-heroku: heroku-login
	heroku container:release web --app ${HEROKU_APP_NAME}

build-ml-api-aws:
	docker build --build-arg PIP_EXTRA_INDEX_URL=${PIP_EXTRA_INDEX_URL} -t udemy-ml-api:latest .

push-ml-api-aws:
	docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/udemy-ml-api

tag-ml-api-aws:
	docker tag udemy-ml-api:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/udemy-ml-api:latest

.PHONY: heroku-login build-ml-api-heroku push-ml-api-heroku tag-ml-api-aws push-ml-api-aws build-ml-api-aws
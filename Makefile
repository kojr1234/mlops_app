# set up the login key using the heroku cli
heroku-login:
	heroku container:login

build-ml-api-heroku: heroku-login # dependecy
	docker build --build-arg PIP_EXTRA_INDEX_URL=${PIP_EXTRA_INDEX_URL} -t registry.heroku.com/${HEROKU_APP_NAME}/web

push-ml-api-heroku: heroku login
	docker push registry.heroku.com/${HEROKU_APP_NAME}/web

release-ml-api-heroku: heroku login
	heroku container:release web --app ${HEROKU_APP_NAME}
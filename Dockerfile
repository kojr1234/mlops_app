FROM python:3.9.12

# create the user (best practice) that will run the app
RUN adduser --disabled-password --gecos '' ml-api-user

WORKDIR /opt/mlops_app

ARG PIP_EXTRA_INDEX_URL

# this command copies from local to target (/opt/mlops_app) directory
ADD ./ /opt/mlops_app/ 

RUN pip install --upgrade pip
RUN pip install -r /opt/mlops_app/requirements.txt

RUN chmod +x /opt/mlops_app/run.sh
# set the user
RUN chown -R ml-api-user:ml-api-user ./

USER ml-api-user

# opens the 8001 port
EXPOSE 8001

CMD ["bash","./run.sh"]
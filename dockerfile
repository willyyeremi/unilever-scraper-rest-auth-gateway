FROM python:3.10.11

USER root

ENV PROJECT_HOME=/home/project_home/project_workdir

RUN useradd -ms /bin/bash project_home && \
    mkdir -p $PROJECT_HOME && \
    chown -R project_home:project_home /home/project_home
WORKDIR $PROJECT_HOME

COPY app/requirements.txt $PROJECT_HOME/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
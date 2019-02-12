FROM python:2.7

RUN pip install setuptools tox flake8

COPY . /asperathos-visualizer/

WORKDIR /asperathos-visualizer

ENTRYPOINT ./run.sh

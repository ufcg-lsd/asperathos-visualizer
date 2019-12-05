FROM python:3.7
COPY ./asperathos-visualizer /asperathos-visualizer
WORKDIR /asperathos-visualizer
RUN pip install setuptools tox flake8
ENTRYPOINT ./run.sh

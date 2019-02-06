# Asperathos - Visualizer

## Overview
The **Visualizer** is the framework responsible for provide to the user a visualization plataform in order to follow the progress of the job launched.

**Asperathos** was developed by the [**LSD-UFCG**](https://www.lsd.ufcg.edu.br/#/) *(Distributed Systems Laboratory at Federal University of Campina Grande)* as one of the existing tools in **EUBra-BIGSEA** ecosystem.

**EUBra-BIGSEA** is committed to making a significant contribution to the **cooperation between Europe and Brazil** in the *area of advanced cloud services for Big Data applications*. See more about in [EUBra-BIGSEA website](http://www.eubra-bigsea.eu/).

## How does it works?
The visualizer is implemented following a **plugin architecture**, providing flexibility to customize your deployment using only the plugins you need, avoiding to include unnecessary dependencies (from others plugins) to your deploy environment.
All the integrations with different infrastructures and components are made by specific plugins.

## How to develop a plugin?
See [plugin-development.md](docs/plugin-development.md).

## How to add a datasource?
See [datasource-addition.md](docs/datasource-addition.md)

## Requirements
* Python 3.5
* Linux packages: python-dev and python-pip
* Python packages: setuptools, tox and flake8

To **apt** distros, you can use [pre-install.sh](pre-install.sh) to install the requirements.

### Configuration
A configuration file is required to run the Visualizer. **Edit and fill your visualizer.cfg in the root of Broker directory.** Make sure you have fill up all fields before run.
You can find a template in [config-example.md](docs/config-example.md).

### Run
In the Visualizer root directory, start the service using run script:
```
$ ./run.sh
```

Or using tox command:
```
$ tox -e venv -- visualizer
```

### Run Unit Tests

## Visualizer REST API
Endpoints are avaliable on [restapi-endpoints.md](docs/restapi-endpoints.md) documentation.

## Avaliable plugins
* [K8s-Grafana](docs/plugins/k8s-grafana.md)

## Avaliable datasources
* [Monasca](docs/datasources/monasca.md)
* [InfluxDB](docs/datasources/influxdb.md)
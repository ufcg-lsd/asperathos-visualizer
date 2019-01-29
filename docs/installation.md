## Requirements
* Python 2.7
* Linux packages: python-dev and python-pip
* Python packages: setuptools, tox and flake8

To **apt** distros, you can use [pre-install.sh](pre-install.sh) to install the requirements.

## Install
Clone the [Visualizer repository](https://github.com/ufcg-lsd/asperathos-visualizer) in your machine.

### Configuration
A configuration file is required to run the Visualizer. **Edit and fill your visualizer.cfg in the root of Visualizer directory.** Make sure you have fill up all fields before run.
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

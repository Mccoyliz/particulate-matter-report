# Particulate Matter Report Project

## Table of Contents
- [Task Description](#task-description)
- [Installation](#installation)
- [Usage](#usage)
- [Ideas for Future Development](#ideas-for-future-development)
- [Further Context](#further-context)
- [References](#references)

## Task Description

We would like you to implement a small program to read live data from the public API https://pm25.lass-net.org/ , perform some simple analysis on it, and generate a report.

Your program should:
- read the data for a device using the /device/<device_id>/history/ endpoint
- Save the data into local persistent storage (what solution you use is up to you)
detect periods where the PM2.5 level goes above the threshold of 30
output a report containing:
  - a list of times when the level when above the danger threshold
  - the daily maximum, daily minimum, and daily average pollution value

If new data becomes available from the API, your solution should insert any new data into the local storage, maintaining any data that is already there.

### My Solution
- **Data Retrieval**: The `requests` library is used to fetch data from the `/device/<device_id>/history/` endpoint for a specific device.
- **Data Storage**: The fetched data is stored in a local SQLite database for persistent storage.
- **Reporting**: The required values are output to an `app.log` file, providing a report of the analyzed data.

### Steps taken to make this solution production ready

- Class structure used.
- Custom exception used for instances when no records are returned from the API.
- Docstrings and typing hints on functions.
- Using poetry to package the project.
- [Makefile](Makefile) created for common commands.
- [Unit tests](tests) and automated documentation.
- [GitHub actions workflow](.github/workflows/test_and_deploy_workflow.yaml) to run tests and create automated docs hosted on GitHub pages.
- [Pull request template](.github/PULL_REQUEST_TEMPLATE.md) file created in the `.github` folder - everytime a PR is opened the description will be autopopulated with this text.

## Prerequisites
If you are running this code on a Windows machine you will need to have WSL installed.

## Installation
- Clone this repo
- Install poetry (run [this script](utils/install-poetry.sh))
```
bash utils/install-poetry.sh
```
- Create a venv for the project 

```
python3 -m venv .venv
```
- Activate the environment
```
source .venv/bin/activate
```
- Install this project `make install`
- Run poetry shell to spawn a shell within the project's virtual environment `poetry shell`
- You can use the following commands to help troubleshoot any installation issues
```
poetry check
poetry debug info
```

## Usage
- Run the [run.py](run.py). If you pass no arguments a default device id and project name will be used.
```
make run
```
If you want to pass a specific device and project name you can do so like this:
```
make run DEVICE_ID="08BEAC0AB11E" PROJECT_NAME="AirBox"
```
- Run the unit tests locally `make test`
- Generate the docs locally `make docs`
- In GitHub a GitHub Actions workflow triggers on changes to the master branch. This will automatically run unit tests and generate project documentation using pdoc then upload it to GitHub pages. 

## Ideas for Future Development
Some ideas for improvements to this project that could be made:
 - Run unit tests with [coverage](https://coverage.readthedocs.io/en/7.5.3/) and add tests so that there is 100% coverage on the repo.
 - Producing a coverage report as a stage in the GitHub actions that is uploaded as a [repo artifact](https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts).
 - Configuring repo settings such that PR's can only be merged when tests pass and minimum coverage percentage is met.
 - Pre commit hooks to run [black](https://github.com/psf/black) and [ruff](https://docs.astral.sh/ruff/) for formatting and linting the code. This avoids contributors commiting code that does not follow code style guidelines.
 - Consider other data store options such as time series databases that might be better options than SQLite, if this solution needs to scale:
   - [QuestDB](https://questdb.io/)
   - [InfluxDB](https://www.influxdata.com/)
   - [TimescaleDB](https://www.timescale.com/)
 - Consider switching from a local data store to a cloud based solution. This could offer high availability, and disaster recovery options - if the one machine this code runs on goes down we will lose all the data.

## Further Context

There are many kinds of air pollution. Some pollution is visible to the naked eye. Most are not. Scientists classify air pollution into two main categories: gasses and suspended particles. The sum of all suspended liquid particles are collectively known as particulate matter.

Particulate matter (PM) is a term used to describe the mixture of solid particles and liquid droplets in the air.

There are several subtypes of inhalable particulate matter. Scientists classify these subtypes by size. Coarse particles with a diameter less than 10 micrometers (μm) are classified as PM10. Fine particles with a diameter of 2.5 μm or less are classified as PM2.5. 
The measuring unit for particulate matter microgram per cubic meter. These fine particles are smaller than one-twenty-eighth of the diameter of a human hair.

What is the relationship between particulate matter and the health of the human body? The size of the particle is the main determinant of where it will lodge in your respiratory system!
Read more [here](https://pm25.lass-net.org/).

## References
- [PM2.5 OPEN DATA PORTAL](https://pm25.lass-net.org/)
- [Poetry](https://python-poetry.org/docs/)
- [Pdoc](https://pdoc.dev/)
- [SQLite](https://www.sqlite.org/docs.html)
- [GitHub Actions](https://docs.github.com/en/actions)

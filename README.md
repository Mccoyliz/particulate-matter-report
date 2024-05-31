# Particulate Matter Report Project

## Table of Contents
- [Task Description](#task-description)
- [Installation](#installation)
- [Usage](#usage)
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

## Installation
- Clone this repo
- Install poetry (there is a utils script in the repo to do this for you)
```
bash utils/install-poetry.sh
```
- Create a venv for the project 

```
python3 -m venv .venv
```
- Activate the environment
```
source.venv/bin/activate
```
- Run poetry install to install this project
```
poetry install
```
- Run poetry shell to spawn a shell within the project's virtual environment
```
poetry shell
```
- You can use the following commands to help troubleshoot any installation issues
```
poetry check
poetry debug info
```

## Usage
- Run the [run.py](run.py) 
- Run the unit tests locally
```
python -m unittest 
```
- In GitHub a GitHub Actions workflow triggers on changes to the master branch. This will automatically run unit tests and generate project documentation using pdoc then upload it to GitHub pages. 

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
- [GitHub Actions](https://docs.github.com/en/actions)

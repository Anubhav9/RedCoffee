[![PyPI Downloads](https://static.pepy.tech/badge/redcoffee)](https://pepy.tech/projects/redcoffee) ![Made with love in Japan](https://madewithlove.now.sh/jp?heart=true) ![Python](https://camo.githubusercontent.com/07858da9ad3cd19f1e10777508bf1b5470f22f8eb0b3ceaa425e2ff85461e30e/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f507974686f6e2d3337373641423f7374796c653d666f722d7468652d6261646765266c6f676f3d707974686f6e266c6f676f436f6c6f723d7768697465) 

# RedCoffee

RedCoffee is a command-line tool designed to manage SonarQube reports easily. It allows you to generate PDF reports from SonarQube analysis data. The project mainly targets SonarQube Community Edition since it lacks the default capability to export PDF reports.

## Installation

To install RedCoffee, you can use pip. First, ensure you have Python and pip installed on your system. Then, you can install RedCoffee directly from PyPI using the following command:

```bash
pip install redcoffee
```

## Pre Requisites

The SonarQube analysis for the project should already have been completed.

## Project Structure

Directory               | Usage                                    |
------------------------|------------------------------------------|
`.github/workflows`       | Github Action Files. <br> i) `trigger-test.yaml` - To Trigger Unit Tests on every commit. <br> ii) `deploy-mkdocs.yaml` - To trigger deployment of mkdocs when something is merged to main / master branch. |
`integrations`            | Contains 3rd Party Integrations <br> i) `IPInfo` - To get the user's GeoLocation Details <br> ii) `Sentry` - For error analysis and logs |
`core`                    | The brain of the repository. The control will ultimately land up here. <br> i) `utils` - Core Utils. Utilities essential for the core functionality to be up and running. <br> ii) `analyser.py` - Most of the SonarQube API Calls being made in this file. |
`reports`                 | Controls the stuff related to look and feel of the generated reports. <br> i)`templating.py` - Code containing the structure of the report. <br> ii) `utils` - Code / Utility functions  essential for the report templating to be up and running. |
`utils`                   | General Utility Functions. 
`tests`                   | Contains the Unit Tests. |

Files                     |    Usage                             |
--------------------------|---------------------------------------|
`redcoffee.py`            | The entrypoint of the project         |
`requirements.txt`        | Includes all necessary libraries required to keep this project up and running |
`docker-compse.yml`       | Brining up the docker containers if someones wants to test out things locally |
`wiremock-using-docker.sh`| Required for Trigger the unit test cases |


## Local Setup

Please note that the project has not been dockerised yet. Hence, it does not contain a DockerFile. However, please ensure that you have Docker installed on your system as we will require the same to have few containers up and running.

To setup RedCoffee locally on your machine, please follow the below steps

* In your terminal, please run the following command : `pip install -r requirements.txt`. This will ensure all the libraries are installed in your system which is essential for the project to be up and running.

* Next, please proceed to run the following docker command : `docker compose -f docker-compose.yml up`. This will ensure you have the required Infra up and running for the project to work successfully. Required Infra over here means `SonarQube Community Edition` and the `Postgres DB`.

* The configured username and password for the database can be found out in the docker compose file.

* Please procced to navigate to `localhost:9000` as this is the address where your SonarQube instance is up and running ( unless you have changed the ports ) . It will ask you for the login. Please enter the username as `admin` and password as `admin`. It will prompt you to re-enter a new password. Please set up a password of your choice.

* Please click on your profile icon ( right most corner ) and click on the Account Section. Navigate to the Security section. Please procced to generate a SonarQube User Token. Please remember to save this token somewhere as you won't be able to see it later.

Please note that due to the unavailability of `IPInfo Access Key` and `Sentry DSN URL` on your local system, the calls for these APIs will fail. However, this does not block the execution.

## Usage

Please run the following command to generate the PDF Report

```bash
redcoffee generatepdf --host=${YOUR_SONARQUBE_HOST_NAME} --project=${SONARQUBE_PROJECT_KEY} --path=${PATH WHERE PDF FILE IS TO BE STORED} --token=${SONARQUBE_USER_TOKEN}
```


## Documentation ( made available via Github Pages )

Please visit the Github Page for this project to stay updated with the latest changes - [Github Page Documentation for RedCoffee](https://anubhav9.github.io/RedCoffee)


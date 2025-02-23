[![PyPI Downloads](https://static.pepy.tech/badge/redcoffee)](https://pepy.tech/projects/redcoffee)

# RedCoffee

RedCoffee is a command-line tool designed to manage SonarQube reports easily. It allows you to configure the SonarQube analysis token and generate PDF reports from SonarQube analysis data.

## Installation

To install RedCoffee, you can use pip. First, ensure you have Python and pip installed on your system. Then, you can install RedCoffee directly from PyPI:

```bash
pip install redcoffee
```

Disclaimer: Due to some changes in response structure of SonarQube API, I had to push a non backward compatible change. Hence, it is advisable to upgrade to redcoffee=1.1
```bash
pip install redcoffee==1.1
```


## Pre Requisites

The SonarQube analysis for the project should have been already done.

## Usage

Please run the following command to generate the PDF Report

```bash
redcoffee generatepdf --host=${YOUR_SONARQUBE_HOST_NAME} --project=${SONARQUBE_PROJECT_KEY} --path=${PATH WHERE PDF FILE IS TO BE STORED} --token=${SONARQUBE_USER_TOKEN}
```

## Maintenance

Please reach out to @Anubhav9 on Github


[![PyPI Downloads](https://static.pepy.tech/badge/redcoffee)](https://pepy.tech/projects/redcoffee) ![Made with love in Japan](https://madewithlove.now.sh/jp?heart=true) ![Python](https://camo.githubusercontent.com/07858da9ad3cd19f1e10777508bf1b5470f22f8eb0b3ceaa425e2ff85461e30e/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f507974686f6e2d3337373641423f7374796c653d666f722d7468652d6261646765266c6f676f3d707974686f6e266c6f676f436f6c6f723d7768697465) 

# RedCoffee

RedCoffee is a command-line tool designed to manage SonarQube reports easily. It allows you to configure the SonarQube analysis token and generate PDF reports from SonarQube analysis data.

## Installation

To install RedCoffee, you can use pip. First, ensure you have Python and pip installed on your system. Then, you can install RedCoffee directly from PyPI:

```bash
pip install redcoffee
```

## Pre Requisites

The SonarQube analysis for the project should have been already done.

## Usage

Please run the following command to generate the PDF Report

```bash
redcoffee generatepdf --host=${YOUR_SONARQUBE_HOST_NAME} --project=${SONARQUBE_PROJECT_KEY} --path=${PATH WHERE PDF FILE IS TO BE STORED} --token=${SONARQUBE_USER_TOKEN}
```

## Documentation ( made available via Github Pages )

Please visit the Github Page for this project to stay updated with the latest changes - [Github Page Documentation for RedCoffee](https://anubhav9.github.io/RedCoffee)


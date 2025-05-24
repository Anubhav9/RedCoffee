import logging
import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth
import platform
from utils.general_utils import handle_protocol_for_every_communication
from utils.general_utils import remove_protocol
import constants
from reports import templating
from integrations.sentry_integration import SentryIntegration
from integrations.sentry_integration import SentryConnectionUnsuccessfulPayload
from integrations.sentry_integration import SentryGeneralUnsuccessfulPayload
from integrations.sentry_integration import SentryGeneralSuccessPayload
from integrations.ipinfo_integration import IPInfoIntegration


load_dotenv()
redcoffee_current_version = "v2.12"
sentry_integration = SentryIntegration(
    os.environ.get("SENTRY_DSN_URL", ""), False, 1.0, 1.0)
ipinfo_integration = IPInfoIntegration(os.environ.get("IP_INFO_ACCESS_TOKEN", ""))


def get_reported_issues_by_sonarqube(host_name, auth_token, project_name, protocol):
    """
    This function makes an API call to SonarQube server and fetches all the information
    about the project which has already been analysed.

    Arguments
    host_name : - The host where SonarQube server has been running
    auth_token : - The token used for authenticating with the API
    project_name " - The project name whose reports we want to fetch

    Returns
    The response of the SonarQube API

    """
    logging.debug("Auth token being used is :: " + auth_token)
    sqa_headers = {"Authorization": "Basic " + auth_token}
    auth = HTTPBasicAuth(auth_token, "")
    logging.debug("Bearer Token being passed is :: " + str(sqa_headers))
    # First Priority goes to protocol supplied, if any
    protocol_type = handle_protocol_for_every_communication(
        protocol, host_name)
    if host_name.startswith("http") or host_name.startswith("http"):
        host_name = remove_protocol(host_name)
    url_to_hit = protocol_type + host_name + \
        "/api/issues/search?componentKeys=" + project_name + "&resolved=false"
    logging.info(
        "URL that has we are hitting to fetch SonarQube reports are " + url_to_hit)
    try:
        response = requests.get(url=url_to_hit, auth=auth)
    except Exception:
        print(
            "We are sorry, we're unable to establish connection with your SonarQube Instance. Please recheck if you have provided the correct host name & port and protocol (if applicable)")

        builder = SentryConnectionUnsuccessfulPayload()
        builder.set_protocol(protocol)
        builder.set_assigned_protocol_type(protocol_type)
        builder.set_redcoffee_version(redcoffee_current_version)
        builder.set_operating_system(platform.system())
        builder.set_country_of_origin(
            ipinfo_integration.get_user_geo_location())
        sentry_unsuccessful_response_payload = builder.get_data()
        sentry_integration.set_context(sentry_unsuccessful_response_payload)
        sentry_integration.capture_message(f"Unfortunately, Report Generation failed because {constants.SENTRY_CONNECTION_UNSUCCESSFUL_MESSAGE}", "error")
        sentry_integration.flush()
        return ""
    if (response.status_code == 200):
        logging.debug(
            "OK Status code is received , moving on to the next operations")
        return response
    elif (response.status_code != 200):
        logging.error(f"Error fetching issues from SonarQube: {response.status_code}")
        sonarqube_version, programming_language = get_info_for_sentry_analysis(
            host_name, project_name, auth_token, protocol)
        is_user_token = False
        token_fragmented = auth_token.split("_")
        if token_fragmented[0] == "squ":
            is_user_token = True

        builder = SentryGeneralUnsuccessfulPayload()
        builder.set_redcoffee_version(redcoffee_current_version)
        builder.set_sonarqube_version(sonarqube_version)
        builder.set_operating_system(platform.system())
        builder.set_major_programming_language(programming_language)
        builder.set_response_code(response.status_code)
        builder.set_is_user_token(is_user_token)
        builder.set_country_of_origin(
            ipinfo_integration.get_user_geo_location())
        sentry_unsuccessful_response = builder.get_data()
        sentry_integration.set_context(sentry_unsuccessful_response)
        sentry_integration.capture_message(f"Unfortunately, Report Generation failed because {constants.SENTRY_GENERAL_UNSUCCESSFUL_MESSAGE}", "error")
        sentry_integration.flush()
        return ""


def get_issues_by_type(response, issue_type):
    """
    This function filters the component to be fixed , what needs to be fixed
    , the line number where fix needs to be made , severity of the issue based on
    the issue type as passed in the argument.

    Argument
    response - The API response of SonarQube
    isse_type_list - The type of issue that needs to be filtered

    Returns
    component_lix , fix_list , line_number , impact , issue_type_list ie the parameters
    that are eventually passed on to the analysis table of SonarQube

    """
    component_list = []
    fix_list = []
    line_number = []
    impact = []
    issue_type_list = []
    response_body = response.json()

    for i in range(0, len(response_body["issues"])):
        actual_issue_type = response_body["issues"][i]["type"]
        if (actual_issue_type == issue_type):
            component_list.append(response_body["issues"][i]["component"])
            fix_list.append(response_body["issues"][i]["message"])
            line_number_get = response_body["issues"][i].get("line")
            if line_number_get is not None:
                line_number.append(line_number_get)
            else:
                line_number.append("NA")
            impact.append(response_body["issues"][i]["severity"])
            issue_type_list.append(issue_type)
    return component_list, fix_list, line_number, impact, issue_type_list


def get_info_for_sentry_analysis(host_name, project_name, auth_token, protocol):
    protocol_type = handle_protocol_for_every_communication(
        protocol, host_name)
    if host_name.startswith("http") or host_name.startswith("http"):
        host_name = remove_protocol(host_name)
    URL_FOR_SONARQUBE_VERSION = f"{protocol_type}{host_name}/api/system/status"
    auth = HTTPBasicAuth(auth_token, "")
    response_body_version = "NOT SET"
    response_for_sonarqube_version = requests.get(
        url=URL_FOR_SONARQUBE_VERSION, auth=auth)
    if response_for_sonarqube_version.status_code == 200:
        response_body_version = response_for_sonarqube_version.json()[
            "version"]
    else:
        logging.info("Some error occurred while getting SonarQube version. However, this does not impact report generation ")

    URL_FOR_MAJOR_LANGUAGE = f"{protocol_type}{host_name}/api/measures/component?component={project_name}&metricKeys=ncloc_language_distribution"
    response_for_major_programming_language = requests.get(
        url=URL_FOR_MAJOR_LANGUAGE, auth=auth)
    language = "NOT SET"
    if response_for_major_programming_language.status_code == 200:
        try:
            all_languages_json = response_for_major_programming_language.json()
            all_languages_component = all_languages_json.get("component", {})
            all_languages_measures = all_languages_component.get("measures")
            if all_languages_measures is None:
                logging.info("SonarQube API didn't respond with correct standards")

            elif all_languages_measures is not None and len(all_languages_measures) > 0:
                all_languages = all_languages_measures[0].get("value")
                if all_languages is not None:
                    all_languages_list = all_languages.split(";")
                    min_val = -1

                    for i in range(0, len(all_languages_list)):
                        sub_factors = all_languages_list[i].split("=")
                        language_per = sub_factors[1]
                        language_per = int(language_per)
                        if (language_per > min_val):
                            min_val = language_per
                            language = sub_factors[0]
                else:
                    logging.info("SonarQube API didn't respond with correct standards")
        except Exception as e:
            logging.info(f"Some error occured either while unpacking the json or in the measures array. Exception being thrown is {e}")
            return response_body_version, language

    else:
        logging.info("Some error occurred while fetching the major programming language. However, this does not impact report generation ")
    return response_body_version, language


def get_duplication_density(host_name, project_name, auth_token, protocol):
    protocol_type = handle_protocol_for_every_communication(
        protocol, host_name)
    if host_name.startswith("http") or host_name.startswith("http"):
        host_name = remove_protocol(host_name)
    DUPLICATION_URL = f"{protocol_type}{host_name}/api/measures/component?component={project_name}&metricKeys=duplicated_lines_density"
    logging.info(f"Generated Duplication URL is :: {DUPLICATION_URL}")
    auth = HTTPBasicAuth(auth_token, "")
    duplication_response = requests.get(url=DUPLICATION_URL, auth=auth)
    if duplication_response.status_code != 200:
        logging.info(f"Something went wrong while fetching the duplication count. Recevied status code is : {duplication_response.status_code}")
        logging.info("INFO : This would not impact your report generation but duplication % will be defaulted as Zero")
        return 0
    else:
        try:
            duplication_response_json = duplication_response.json()
            duplicated_component = duplication_response_json.get("component")
            if duplicated_component is None:
                return 0
            else:
                duplicated_measures = duplicated_component.get("measures")
                if duplicated_measures is not None and len(duplicated_measures) > 0:
                    duplicated_line_density = duplicated_measures[0].get(
                        "value")
                    if duplicated_line_density is None:
                        return 0
                    else:
                        logging.info(f"The duplication % received is :: {duplicated_line_density}")
                        return duplicated_line_density
                else:
                    return 0
        except Exception:
            logging.info("For Some reasons duplication % cannot be computed")
            return 0


def generate_final_report_and_transmit_to_sentry(file_path, host_name, project_name, auth_token, protocol):
    result=templating.create_issues_report(
        file_path, host_name, auth_token, project_name, protocol)
    if result==0:
        return ""
    sonarqube_version, programming_language = get_info_for_sentry_analysis(
        host_name, project_name, auth_token, protocol)
    builder = SentryGeneralSuccessPayload()
    builder.set_redcoffee_version(redcoffee_current_version)
    builder.set_sonarqube_version(sonarqube_version)
    builder.set_operating_system(platform.system())
    builder.set_major_programming_language(programming_language)
    builder.set_country_of_origin(ipinfo_integration.get_user_geo_location())
    sentry_successful_response_payload = builder.get_data()
    sentry_integration.set_context(sentry_successful_response_payload)
    sentry_integration.capture_message("Report has been generated successfully", "info")
    sentry_integration.flush()
    print("🎉Report Generated Successfully🍻")

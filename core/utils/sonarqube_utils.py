import logging
import requests
from requests.auth import HTTPBasicAuth
from utils import general_utils
from utils.general_utils import handle_protocol_for_every_communication


def get_duplication_map(host_name, project_name, auth_token, protocol):
    protocol_type = handle_protocol_for_every_communication(
        protocol, host_name)
    if host_name.startswith("http") or host_name.startswith("https"):
        host_name = general_utils.remove_protocol(host_name)
    DUPLICATION_URL = f"{protocol_type}{host_name}/api/measures/component_tree?component={project_name}&metricKeys=duplicated_lines"
    logging.info(f"Generated Duplication URL is :: {DUPLICATION_URL}")
    auth = HTTPBasicAuth(auth_token, "")
    duplication_response = requests.get(url=DUPLICATION_URL, auth=auth)
    if duplication_response.status_code != 200:
        logging.info(
            f"Something went wrong while fetching the duplication count. Recevied status code is : {duplication_response.status_code}")
        logging.info(
            "INFO : This would not impact your report generation but duplication table won't be visible to you")
        return {}
    else:
        try:
            duplication_map = {}
            duplication_response_json = duplication_response.json()
            duplication_files_component = duplication_response_json.get(
                "components")
            if duplication_files_component is None:
                logging.info(
                    "SonarQube API didn't respond with correct standard since Component Key is missing within Duplication Response")
                return {}
            else:
                if (len(duplication_files_component) > 0):
                    for i in range(0, len(duplication_files_component)):
                        duplication_file_measures = duplication_files_component[i].get(
                            "measures")
                        if duplication_file_measures is None:
                            logging.info(
                                "SonarQube API didn't respond in the correct format since it does not have a measure component in duplication API")

                        else:
                            if (len(duplication_file_measures) > 0):
                                duplicated_line_count = duplication_file_measures[0].get(
                                    "value")
                                if duplicated_line_count is not None:
                                    if int(duplicated_line_count) > 0:
                                        file_name = duplication_files_component[i]["path"]
                                        duplication_map.update(
                                            {file_name: duplicated_line_count})
                                        logging.info(duplication_map)
                                else:
                                    logging.info(
                                        "SonarQube API didn't respond in the correct format since we didn't get duplication count")
                            else:
                                logging.info(
                                    "SonarQube API didn't respond in the correct format since measures is not a list in duplication API")
                    return duplication_map
                else:
                    logging.info(
                        "SonarQube API didn't respond in correct format since Component is not returned as a list or size of component list is 0")
                    return {}
        except Exception:
            logging.info(
                "For some reasons, duplication map cannot be generated")
            return {}

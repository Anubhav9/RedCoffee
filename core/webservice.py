import requests
import logging
from urllib.parse import urljoin
from requests.auth import HTTPBasicAuth

class WebService:
    def __init__(self, auth_token, protocol_type, host_name, project_name):
        self.auth_token = auth_token
        self.auth = HTTPBasicAuth(self.auth_token, "")
        self.sqa_headers = {"Authorization": "Basic " + auth_token}
        self.base_url = f"{protocol_type}{host_name}"
        self.project_name = project_name
        self.health_check()
    
    
    def health_check(self):
        try:
            logging.debug(f"Auth token being used is :: {self.auth_token}")
            logging.debug(f"Bearer Token being passed is :: {str(self.sqa_headers)}")
            response = requests.get(self.base_url)
            response.raise_for_status()
        except Exception as e:
            logging.debug(f"Healthcheck failed: {e}")


    def get_unresolved_issues(self, page=1):
        ''''
            This function get the issues with resolved arg equals to false.
            Arguments:
                - page: Default argument to get the first page of issues
            Returns:
                Request response
        '''

        api_path = f"/api/issues/search"
        url_to_hit = urljoin(self.base_url, api_path)

        api_parameters = {
            "componentKeys": self.project_name,
            "resolved": "false",
            "p": page
        }

        response = requests.get(url=url_to_hit, auth=self.auth, params=api_parameters)

        return response
    

    def get_all_unresolved_issues(self, total: int, page_size: int) -> list:
        ''''
            This function iterates over the total issues, using the page_size
            argument to decrease his value. This will ensure all issues in the report.
        '''

        response_list = []
        issues_total = total
        page_counter = 1
        status_code = 0
        
        while issues_total > 0:
            try:
                response = self.get_unresolved_issues(page=page_counter)
                response.raise_for_status()

                logging.info(f"URL that has we are hitting to fetch SonarQube reports are {response.url}")
                response_list.append(response)
                issues_total -= page_size
                page_counter += 1

            except requests.exceptions.HTTPError as e:
                logging.debug(f"Failed to get all unresolved issues: {e}")
                return list(), status_code

        status_code = 200

        return response_list, status_code


    def get_total_issues(self, request_function):
        '''
            This function get the total issues from your SonarQube project.
            This information will be used to feed a while loop to get all the issues

            Argument:
                - request_function: The function used to get the issues

            Returns:
                - total: The integer value for total issues
                - ps: The default page size returned by api
        '''
        
        try:
            response = request_function()
            response.raise_for_status()
            response = response.json()

            total, ps = response["total"], response["ps"]

            return total, ps
        except requests.exceptions.HTTPError as e:
            logging.debug(f"Failed to get total issues: {e}")

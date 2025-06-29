from diagnose import constants
import requests
from utils import general_utils

def check_all_functioning_parameters(protocol,host,token):
    """
    Check if all the parameters are functioning correctly.
    """    
    total_checks = 3
    successful_checks = 0
    unsuccessful_checks = 3
    confirm_if_user_token = token.startswith("squ_")
    if confirm_if_user_token:
        print(constants.MESSAGE_BASE_SONARQUBE_USER_TOKEN)
        successful_checks=successful_checks+1
    else:
        
        print(constants.MESSAGE_SONARQUBE_NOT_A_USER_TOKEN)
        print(constants.MESSAGE_SONARQUBE_USER_TOKEN_HINT_MESSAGE)
        print(constants.MESSAGE_SONARQUBE_USER_TOKEN_GENERATION_STEPS)

    try:
        healthcheck_response= requests.get(f"{protocol}{host}{constants.HEALTHCHECK_ENDPOINT}",auth=(token,""))
        if healthcheck_response.status_code == 200:
            status = healthcheck_response.json()["health"]
            if status == "GREEN" or status == "YELLOW":
                successful_checks=successful_checks+1
                print(constants.MESSAGE_SONARQUBE_SERVER_REACHABLE)
                authenticate_token = requests.get(f"{protocol}{host}/api/authentication/validate",auth=(token,""))
                if authenticate_token.status_code == 200:
                    token_result = authenticate_token.json()["valid"]
                    if token_result == True:
                        successful_checks=successful_checks+1
                        print(constants.MESSAGE_USER_TOKEN_VALIDATED)
                    else:
                        print(constants.MESSAGE_USER_TOKEN_SOMETHING_WRONG)
                else:
                    authentication_status_code = authenticate_token.status_code
                    if authentication_status_code == 401:
                        print(constants.MESSAGE_USER_TOKEN_401)
                    elif authentication_status_code == 403:
                        print(constants.MESSAGE_USER_TOKEN_403)
                    else:
                        print(constants.MESSAGE_USER_TOKEN_SOMETHING_WRONG)
        else:
            print(constants.MESSAGE_SONARQUBE_SERVER_UNREACHABLE)
            print(constants.MESSAGE_SONARQUBE_SERVER_UNREACHABLE_HINT_MESSAGE)
        
        print(f"Final Diagnosis: {successful_checks} out of {total_checks} checks passed.")
    except Exception as e:
        print(constants.MESSAGE_SONARQUBE_SERVER_UNREACHABLE)
        print(constants.MESSAGE_SONARQUBE_SERVER_UNREACHABLE_HINT_MESSAGE)
        print(f"Diagnosis Failed. Only able to validate SonarQube User Token. Passed {successful_checks} and rest cannot be validated")
        

def connect_for_support():
    """
    Connect for support. Opening Github Issues or shooting an email
    """
    print(constants.MESSAGE_SUPPORT_APOLOGIES)
    print(constants.MESSAGE_SUPPORT_DIAGNOSE_COMMAND)
    print(constants.MESSAGE_SUPPORT_EMAIL)

import logging
from pathlib import Path
from urllib.parse import urlparse
import constants
import os

def check_and_validate_file_path(path):
    """
    Sanitise file path and checks if it is a valid directory to store the generated report.

    Arguments:
        path: The file path being provided by the user
    """
    if path is None:
        create_redcoffee_report_directory()
        resolved_directory = Path.home() / "redcoffee-reports" / constants.FALLBACK_FILE_NAME
        return resolved_directory

    else:
        resolved_directory = ""
        result_ends_with_pdf = str(path).endswith(".pdf")
        if result_ends_with_pdf == False:
            resolved_directory = Path(path) / constants.FALLBACK_FILE_NAME
            return check_and_validate_file_path(resolved_directory)

        else:
            path_resolved = Path(path).resolve(strict=False)
            if path_resolved.parent.exists():
                logging.info(
                    "Since Path is valid and exists, we are not manipulating things at Server Side")
                resolved_directory = path
                return resolved_directory
            else:
                create_redcoffee_report_directory()
                resolved_directory = Path.home() / "redcoffee-reports" / constants.FALLBACK_FILE_NAME
                return resolved_directory


def handle_protocol_for_every_communication(protocol, host):
    """
    Observed a lot of errors related to protocol since I was enforcing protocol based on custom logic which was incorrect. Figured out a temporary way to handle the protocol communication by adding extra parameter in click command which is optional currently. If this works out, I will promote this to required argument in the next major release - 2.5 onwards.

    Arguments:
        protocol - Only 2 available choices - http or https
    """

    if protocol == "" or protocol is None:
        logging.info(
            "No protocol has been supplied, hence we will go to fallback routes")
        protocol_type = ""
        if "localhost" in host:
            protocol_type = "http://"
        elif host.startswith("http://") or host.startswith("https://"):
            squandered_string = host.split(":")[0]
            protocol_type = squandered_string + "://"
        else:
            protocol_type = "http://"

        if "localhost" in host and host.startswith("https://"):
            protocol_type = "http://"
        return protocol_type

    else:
        logging.info(f"Protocol Supplied is {protocol}")
        protocol_type = protocol + "://"
        return protocol_type


def remove_protocol(url):
    """
    Remove the protocol from the URL
    """
    parsed_url = urlparse(url)
    return parsed_url.netloc + parsed_url.path


def create_redcoffee_report_directory():
    """
    Create the redcoffee-reports directory
    """
    try:
        os.makedirs(os.path.join(Path.home(), "redcoffee-reports"), exist_ok=True)
    except Exception as e:
        logging.info(f"Error creating redcoffee-reports directory: {e}")
    
    

import sys
import os
from time import sleep
from pathlib import Path

import pytest
import subprocess
from core import analyser
from core.utils.sonarqube_utils import get_duplication_map
from utils.general_utils import check_and_validate_file_path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture(scope="session", autouse=True)
def spawn_up_wiremock_server():
    print("Trigger Shell Command to bring up WireMock Container")
    subprocess.call(['sh', './wiremock_using_docker.sh'])
    sleep(10)
    # Example: Start WireMock, setup database connection


""""
def test_get_issues_by_type():
    mock_response=Mock()
    file=open("tests/sample_response.json")
    data=json.load(file)
    mock_response.json.return_value = data
    component_list, fix_list, line_number, impact, issue_type_list = get_issues_by_type(mock_response, "CODE_SMELL")
    expected_component_list=["app.py","app.py"]
    expected_line_list=[27,27]
    expected_impact_list=["LOW","MEDIUM"]
    ##assert component_list == expected_component_list
    assert line_number==expected_line_list
    assert impact==expected_impact_list

"""


def test_duplicate_line_density():
    duplicate_line_density_actual = analyser.get_duplication_density(
        "localhost:8000", "car-loan-portal", "squ_aa9488007125b09c46e8e2a16a5bccd822738bc2", "http")
    duplicate_line_density_expected = "15.0"
    assert duplicate_line_density_actual == duplicate_line_density_expected, "Actual Duplicate Line Density and Expected Duplicate Line Density does not match"


def test_duplicate_lines():
    actual_duplicate_lines_map = get_duplication_map(
        "localhost:8000", "car-loan-portal", "squ_aa9488007125b09c46e8e2a16a5bccd822738bc2", "http")
    expected_duplicate_lines_map = {"app.py": "60"}
    assert actual_duplicate_lines_map == expected_duplicate_lines_map, "Difference in Hash Map found for Actual Duplicated Line Map and Expected Duplicated Line Map"


@pytest.mark.parametrize("path_name,case", [
    ("car-loan-report.pdf", "file_name_with_pdf"),
    ("car-loan-report", "file_name_without_pdf_extenstion"),
    ("/Uxser", "invalid_directory_name"),
    ("/Uxser/car-loan-report.pdf", "invalid_directory_name_ending_with_pdf"),
    (Path.home() / "Desktop", "random")
])
def test_path_validation(path_name, case):
    returned_result = check_and_validate_file_path(path_name)
    if case == "file_name_wit_pdf":
        assert returned_result == "car-loan-report.pdf", "Mismatch in Path found"
    elif case == "invalid_directory_name" or case == "invalid_directory_name_ending_with_pdf":
        resolved_path = Path.home() / "Downloads" / "generated-sonarqube-report.pdf"
        assert returned_result == resolved_path, "Mismatch in Path found"
    elif case == "random":
        resolved_path = Path.home() / "Desktop" / "generated-sonarqube-report.pdf"
        assert returned_result == resolved_path, "Mismatch in Path found"

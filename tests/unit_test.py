import sys
import os
from time import sleep

import pytest
from unittest.mock import Mock
import json
import subprocess
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from redcoffee import get_issues_by_type, get_duplication_density, get_duplication_map


@pytest.fixture(scope="session", autouse=True)
def spawn_up_wiremock_server():
    print(f"Trigger Shell Command to bring up WireMock Container")
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
    duplicate_line_density_actual=get_duplication_density("localhost:8000","car-loan-portal","squ_aa9488007125b09c46e8e2a16a5bccd822738bc2")
    duplicate_line_density_expected="15.0"
    assert duplicate_line_density_actual==duplicate_line_density_expected,f"Actual Duplicate Line Density and Expected Duplicate Line Density does not match"

def test_duplicate_lines():
    actual_duplicate_lines_map=get_duplication_map("localhost:8000","car-loan-portal","squ_aa9488007125b09c46e8e2a16a5bccd822738bc2")
    expected_duplicate_lines_map={"app.py":"60"}
    assert actual_duplicate_lines_map==expected_duplicate_lines_map,f"Difference in Hash Map found for Actual Duplicated Line Map and Expected Duplicated Line Map"

import sys
import os
import pytest
from unittest.mock import Mock
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from redcoffee import get_issues_by_type


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

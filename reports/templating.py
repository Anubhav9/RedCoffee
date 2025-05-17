from reportlab.platypus import Paragraph, Table, SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import datetime
import logging
from html import escape
import constants
from reports.utils.report_utils import draw_severity_icon
import styling
from styling import BRANDING_STYLE
from core import analyser
from core.utils.sonarqube_utils import get_duplication_map

normal_style = styling.NORMAL_STYLE
header_style = styling.HEADER_STYLE


def create_basic_project_details_table(project_name):
    """
    Creates the table for Basic Project Details

    Arguments:
    project_name : The name of the project for which PDF Report needs to be made

    Returns
    The tabular project structure consisting of basic details
    """

    data_project_basic_details = [
        [Paragraph(constants.TABLE_HEADER_PROJECT_NAME, header_style),
         Paragraph(constants.TABLE_HEADER_ANALYSIS, header_style),
         Paragraph(constants.TABLE_HEADER_BRANCH, header_style)]
    ]
    data_project_basic_details.append([
        Paragraph(project_name, normal_style),
        Paragraph(datetime.datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"), normal_style),
        Paragraph("Main / Master", normal_style)
    ])

    table_basic_details = Table(data_project_basic_details,
                                colWidths=[2 * inch, 3 * inch, 1 * inch, 2.5 * inch, 0.75 * inch])
    table_basic_details.setStyle(styling.TABLE_STYLE)
    return table_basic_details


def actual_table_content_data(component_list, fix_list, line_number_list, impact, issue_type_list):
    """
    Creates the table content for all the information regarding the vulnerabilities detected

    Arguments:
    components_list : The list of components where vulnerabilites have been detected
    fix_list : The fixes that needs to be done in the specific component
    line_number_list : The line number where fix needs to be made / vulnerability detected
    impact : The impact of the vulnerability
    issue_type_list : The type of vulnerability that has been detected

    Returns:
    The tabular data containing all information about the vulnerabilities detected
    """

    data = [
        [Paragraph(constants.TABLE_HEADER_SEVERITY, header_style),
         Paragraph(constants.TABLE_HEADER_DESCRIPTION, header_style),
         Paragraph(constants.TABLE_HEADER_TYPE, header_style),
         Paragraph(constants.TABLE_HEADER_FILE_NAME, header_style),
         Paragraph(constants.TABLE_HEADER_LINE_NUMBER, header_style)]
    ]

    # Table content
    logging.info("Total Issues detected are " + str(len(component_list)))
    for i in range(0, len(component_list)):
        severity_icon = draw_severity_icon(impact[i])
        description = fix_list[i]
        file_name = "/".join(component_list[i].split(":")[1:])
        line_number = str(line_number_list[i])
        issue_type_entry_table = issue_type_list[i]
        issue_type_entry_table = issue_type_entry_table.replace(
            "_", " ").title()

        data.append([
            Paragraph(severity_icon, normal_style),
            Paragraph(escape(description), normal_style),
            Paragraph(escape(issue_type_entry_table), normal_style),
            Paragraph(escape(file_name), normal_style),
            Paragraph(escape(line_number), normal_style),
        ])

    # Create table
    table = Table(data, colWidths=[0.75 * inch,
                  3 * inch, 1 * inch, 2.5 * inch, 0.75 * inch])
    table.setStyle(styling.TABLE_STYLE)
    return table


def duplication_table(duplication_map):
    """
    Creates the table for Duplication

    Arguments:
    duplication_map : The map of the file name and the number of duplicated lines

    Returns:
    The tabular data containing the duplication information
    """

    data = [
        [
            Paragraph(constants.TABLE_HEADER_FILE_NAME, header_style),
            Paragraph(constants.TABLE_HEADER_DUPLICATED_LINES, header_style)]
    ]
    for i, j in duplication_map.items():
        file_name = i
        duplicated_lines = j
        data.append([
            Paragraph(escape(file_name), normal_style),
            Paragraph(escape(duplicated_lines), normal_style),
        ])

    table = Table(data, colWidths=[3 * inch, 1 * inch])
    table.setStyle(styling.TABLE_STYLE)
    return table


def issue_summary_overview(bug_list, vulnerability_list, code_smell_list, duplication_list):
    """
    Creates the table content for the executive summary of the report

    Arguments:
    bug_list: Integer containing number of bugs found during the SonarQube analysis.
    vulnerability_list : Integer containing number of vulnerabilities found during the analysis.
    code_smell_list : Integer containing number of Code Smell found during the analysis.
    duplication list: Dummy as of now, always prints 0%. But ideally should give the duplication percentage.


    Returns:
    The tabular data containing the executive summary for the report.
    """

    data = [
        [Paragraph(constants.TABLE_HEADER_SUMMARY_BUGS, header_style),
         Paragraph(constants.TABLE_HEADER_SUMMARY_VULNERABILITIES, header_style),
         Paragraph(constants.TABLE_HEADER_SUMMARY_CODE_SMELLS, header_style),
         Paragraph(constants.TABLE_HEADER_SUMMARY_DUPLICATION_PER, header_style)
         ]
    ]

    # Table content

    data.append([
        Paragraph(escape(str(bug_list)), normal_style),
        Paragraph(escape(str(vulnerability_list)), normal_style),
        Paragraph(escape(str(code_smell_list)), normal_style),
        Paragraph(escape(str(duplication_list)), normal_style),
    ])

    # Create table
    table = Table(data, colWidths=[2 * inch, 2 * inch, 2 * inch, 2 * inch])
    table.setStyle(styling.TABLE_STYLE)
    return table


def create_issues_report(file_path, host_name, auth_token, project_name, protocol):
    response = analyser.get_reported_issues_by_sonarqube(
        host_name, auth_token, project_name, protocol)
    if (response == ""):
        logging.info(
            "We are sorry, we're having trouble generating your report")
        print("We are sorry, we're having trouble generating your report")
        return 0
    duplication_response = analyser.get_duplication_density(
        host_name, project_name, auth_token, protocol)
    duplication_map = get_duplication_map(
        host_name, project_name, auth_token, protocol)
    component_list, fix_list, line_number_list, impact, issue_type_list = analyser.get_issues_by_type(
        response, "CODE_SMELL")
    size_of_code_smell_list = len(component_list)
    component_list_vulnerability, fix_list_vulnerability, line_number_list_vulnerability, impact_vulnerability, issue_type_list_vulnerability = analyser.get_issues_by_type(
        response, "VULNERABILITY")
    size_of_vulnerability_list = len(component_list_vulnerability)
    component_list_bug, fix_list_bug, line_number_list_bug, imact_bug, issue_type_list_bug = analyser.get_issues_by_type(
        response, "BUG")
    size_of_bug_list = len(component_list_bug)

    component_list = component_list + component_list_vulnerability + component_list_bug
    fix_list = fix_list + fix_list_vulnerability + fix_list_bug
    line_number_list = line_number_list + \
        line_number_list_vulnerability + line_number_list_bug
    impact = impact + impact_vulnerability + imact_bug
    issue_type_list = issue_type_list + \
        issue_type_list_vulnerability + issue_type_list_bug

    doc = SimpleDocTemplate(file_path, pagesize=letter)

    # Custom styles
    title_style = styling.TITLE_STYLE
    subtitle_style = styling.SUBTITLE_STYLE
    elements = []
    elements.append(Paragraph(constants.CREATOR_CREDIT, BRANDING_STYLE))
    elements.append(Paragraph("", title_style))
    # Title
    elements.append(Paragraph(constants.DOCUMENT_HEADER, title_style))
    table_basic_details = create_basic_project_details_table(project_name)
    elements.append(table_basic_details)
    elements.append(Paragraph("", title_style))

    # Summary Section
    elements.append(
        Paragraph(constants.TABLE_HEADER_REPORT_SUMMARY, title_style))
    report_summary = issue_summary_overview(size_of_bug_list, size_of_vulnerability_list, size_of_code_smell_list,
                                            duplication_response)
    elements.append(report_summary)
    elements.append(Paragraph("", title_style))

    # Subtitle
    elements.append(Paragraph(constants.SUBHEADER_DOCUMENT, subtitle_style))
    table = actual_table_content_data(
        component_list, fix_list, line_number_list, impact, issue_type_list)
    elements.append(table)
    elements.append(Paragraph("", title_style))

    # Duplication
    if (len(duplication_map) > 0):
        elements.append(
            Paragraph(constants.SUBHEADER_DUPLICATION_DOCUMENT, subtitle_style))
        table = duplication_table(duplication_map=duplication_map)
        elements.append(table)

    doc.build(elements)

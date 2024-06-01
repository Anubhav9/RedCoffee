import requests
import logging
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
from reportlab.lib.styles import getSampleStyleSheet
import click
import styling
import constants

def get_reported_issues_by_sonarqube(host_name,auth_token,project_name):
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
    logging.debug("Auth token being used is :: "+auth_token)
    sqa_headers={"Authorization": "Bearer "+auth_token}
    logging.debug("Bearer Token being passed is :: "+str(sqa_headers))
    if "localhost" in host_name:
        protocol_type="http://"
    else:
        protocol_type="https://"
    url_to_hit=protocol_type+host_name+"/api/issues/search?componentKeys="+project_name+"&resolved=false"
    logging.info("URL that has we are hitting to fetch SonarQube reports are "+url_to_hit)
    response=requests.get(url=url_to_hit,headers=sqa_headers)
    if(response.status_code==200):
        logging.debug("OK Status code is received , moving on to the next operations")
        return response
    elif(response.status_code!=200):
        logging.error("Status code is "+str(response.status_code))
        return ""


def get_issues_by_type(response,issue_type):
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
    component_list=[]
    fix_list=[]
    line_number=[]
    impact=[]
    issue_type_list=[]
    response_body=response.json()
    
    for i in range(0,len(response_body["issues"])):
        actual_issue_type=response_body["issues"][i]["type"]
        if(actual_issue_type==issue_type):
            component_list.append(response_body["issues"][i]["component"])
            fix_list.append(response_body["issues"][i]["message"])
            line_number.append(response_body["issues"][i]["line"])
            impact.append(response_body["issues"][i]["impacts"][0]["severity"])
            issue_type_list.append(issue_type)        
    return component_list,fix_list,line_number,impact,issue_type_list


def draw_severity_icon(severity):
    """
    Visually generates a circular icon based on severity of the bug.
    Critical -> Red Color
    High -> Orange
    Medium -> Teal
    Low / Default -> Green

    Arguments
    severity : The importance of the bug detected by SonarQube
    """
    if severity == "CRITICAL":
        return "<font color='red' size='12'>&#9679;</font>"
    elif severity == "HIGH":
        return "<font color='orange' size='12'>&#9679;</font>"
    elif severity == "MEDIUM":
        return "<font color='teal' size='12'>&#9679;</font>"
    else:  # Low
        return "<font color='green' size='12'>&#9679;</font>"

def create_issues_report(file_path, host_name, auth_token, project_name):
    response = get_reported_issues_by_sonarqube(host_name, auth_token, project_name)
    if(response==""):
        logging.error("We are sorry, we're having trouble generating your report")
        return
    component_list, fix_list, line_number_list, impact , issue_type_list = get_issues_by_type(response, "CODE_SMELL")
    component_list_vulnerability, fix_list_vulnerability, line_number_list_vulnerability, impact_vulnerability,issue_type_list_vulnerability = get_issues_by_type(response, "VULNERABILITY")
    component_list.append(component_list_vulnerability)
    fix_list.append(fix_list_vulnerability)
    line_number_list.append(line_number_list_vulnerability)
    impact.append(impact_vulnerability)
    issue_type_list.append(issue_type_list_vulnerability)

    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = styling.TITLE_STYLE
    subtitle_style = styling.SUBTITLE_STYLE
    elements = []
    # Title
    elements.append(Paragraph(constants.DOCUMENT_HEADER, title_style))
    table_basic_details=create_basic_project_details_table(project_name)
    elements.append(table_basic_details)
    elements.append(Paragraph("",title_style))
    
    # Subtitle
    elements.append(Paragraph(constants.SUBHEADER_DOCUMENT, subtitle_style))
    table=actual_table_content_data(component_list, fix_list, line_number_list, impact , issue_type_list)
    elements.append(table)
    doc.build(elements)

def create_basic_project_details_table(project_name):
    """
    Creates the table for Basic Project Details

    Arguments:
    project_name : The name of the project for which PDF Report needs to be made

    Returns
    The tabular project structure consisting of basic details
    """
    normal_style = styling.NORMAL_STYLE
    header_style = styling.HEADER_STYLE

    data_project_basic_details = [
        [Paragraph(constants.TABLE_HEADER_PROJECT_NAME, header_style), 
         Paragraph(constants.TABLE_HEADER_ANALYSIS, header_style), 
         Paragraph(constants.TABLE_HEADER_BRANCH, header_style)] 
    ]
    data_project_basic_details.append([
            Paragraph(project_name, normal_style),
            Paragraph(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), normal_style),
            Paragraph("Main / Master", normal_style)
        ])
    
    table_basic_details = Table(data_project_basic_details, colWidths=[2 * inch, 3 * inch, 1 * inch, 2.5 * inch, 0.75 * inch])
    table_basic_details.setStyle(styling.TABLE_STYLE)
    return table_basic_details

def actual_table_content_data(component_list, fix_list, line_number_list, impact , issue_type_list):
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
    normal_style = styling.NORMAL_STYLE
    header_style = styling.HEADER_STYLE
    data = [
        [Paragraph(constants.TABLE_HEADER_SEVERITY, header_style), 
         Paragraph(constants.TABLE_HEADER_DESCRIPTION, header_style), 
         Paragraph(constants.TABLE_HEADER_TYPE, header_style), 
         Paragraph(constants.TABLE_HEADER_FILE_NAME, header_style), 
         Paragraph(constants.TABLE_HEADER_LINE_NUMBER, header_style)]
    ]

    # Table content
    print("Total Issues detected are "+str(len(component_list)))
    for i in range(0,len(component_list)-1):
        severity_icon = draw_severity_icon(impact[i])
        description = fix_list[i]
        file_name = "/".join(component_list[i].split("/")[1:])
        line_number = str(line_number_list[i])
        issue_type_entry_table=issue_type_list[i]

        data.append([
            Paragraph(severity_icon, normal_style),
            Paragraph(description, normal_style),
            Paragraph(issue_type_entry_table, normal_style),
            Paragraph(file_name, normal_style),
            Paragraph(line_number, normal_style),
        ])

    # Create table
    table = Table(data, colWidths=[0.75 * inch, 3 * inch, 1 * inch, 2.5 * inch, 0.75 * inch])
    table.setStyle(styling.TABLE_STYLE)
    return table




@click.group()
def cli():
    pass





@click.command()
@click.option("--host",help="The host url where SonarQube server is running")
@click.option("--project",help="Name of the Project Key that we want to search for in SonarQube report ")
@click.option("--path",help="Path where we want to the PDF Report")
@click.option("--token",help="SonarQube Global Analysis Token")
def generatepdf(host,project,path,token):
    create_issues_report(path,host,token,project)
    

cli.add_command(generatepdf)
if __name__=="__main__":
    cli()


import click
from support import pick_random_support_message, warning_for_path_change
from dotenv import load_dotenv
from utils import general_utils
from core import analyser
from diagnose import sanity
from ascii_art import welcome_banner

load_dotenv()


@click.group()
def cli():
    pass


@click.command()
@click.option("--host", help="The host url where SonarQube server is running", required=True)
@click.option("--project", help="Name of the Project Key that we want to search for in SonarQube report ",
              required=True)
@click.option("--path", help="Path where we want to the PDF Report", required=False)
@click.option("--token", help="SonarQube Global Analysis Token", required=True)
@click.option("--protocol", type=click.Choice(["http", "https"], case_sensitive=False), required=False,
              help="The protocol that you want to enforce - HTTP or HTTPS")
def generatepdf(host, project, path, token, protocol):
    welcome_banner.generate_welcome_banner()
    resolved_path = str(general_utils.check_and_validate_file_path(path))
    analyser.generate_final_report_and_transmit_to_sentry(
        resolved_path, host, project, token, protocol)
    print(pick_random_support_message())
    if path != resolved_path:
        print(warning_for_path_change(resolved_path))

@click.command()
@click.option("--host", help="The host url where SonarQube server is running", required=True)
@click.option("--token", help="SonarQube Global Analysis Token", required=True)
@click.option("--protocol", type=click.Choice(["http", "https"], case_sensitive=False), required=False,
              help="The protocol that you want to enforce - HTTP or HTTPS")
def diagnose(protocol,host,token):
    welcome_banner.generate_welcome_banner()
    new_host = general_utils.remove_protocol(host)
    new_protocol = general_utils.handle_protocol_for_every_communication(protocol,new_host)
    sanity.check_all_functioning_parameters(new_protocol,new_host,token)

@click.command()
def support():
    welcome_banner.generate_welcome_banner()
    sanity.connect_for_support()


cli.add_command(generatepdf)
cli.add_command(diagnose)
cli.add_command(support)
if __name__ == "__main__":
    cli()

import click
from support import pick_random_support_message, warning_for_path_change
from dotenv import load_dotenv
from utils import general_utils
from core import analyser
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
    resolved_path = str(general_utils.check_and_validate_file_path(path))
    analyser.generate_final_report_and_transmit_to_sentry(
        resolved_path, host, project, token, protocol)
    print(pick_random_support_message())
    if path != resolved_path:
        print(warning_for_path_change(resolved_path))


cli.add_command(generatepdf)
if __name__ == "__main__":
    cli()

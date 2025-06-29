import pyfiglet
import colorama
from ascii_art import constants

def generate_welcome_banner():
    """
    Generate a welcome banner using pyfiglet and colorama.
    """
    banner = pyfiglet.figlet_format(constants.REDCOFFEE_BANNER_TEXT)
    colored_banner = colorama.Fore.RED + banner
    print(colored_banner,end="")
    sub_text = colorama.Fore.YELLOW + constants.REDCOFFEE_SUB_TEXT
    print(sub_text)
    print("\n")
    print(colorama.Style.RESET_ALL)



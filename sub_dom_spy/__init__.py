import requests
import time
import urllib3
import logging
import sys
import inspect

import inspy_logger

version = 1.0

PROG_NAME = "SubDomSpy"

logger_names = []


def _add_logger_(logger):
    if not logger in logger_names:
        logger_names.append(logger)


def start_logger(name=None, verbose=True):

    # Set a 'log' attribute that starts with a value of None
    log = None

    # Query the logger instance and see if the 'started' attribute has been set to True or not.
    #
    # If not, start a new root logger using PROG_NAME as it's name. Here we'll pass the 'verbose'
    # parameter to inspy_logger.start() as well.
    if not inspy_logger.started:
        name = str(f"{PROG_NAME}.StartLogger")
        inspy_logger.start(PROG_NAME, verbose)
        log = logging.getLogger(name)
        log.info(f"Logging started for {PROG_NAME}!")

    else:

        # If they fail to provide a name for a child-logger we'll just grab the name of the calling
        # function.
        if name is None:
            name = inspect.stack()[1].function

            # Then we'll prettify it so it sticks in with the format of the rest of the logs.
            # First, split it into a list
            name_ls = name.split("_")

            # Take each 'word' in that list (strings that were separated by '_') and capitalize it.
            for word in name_ls:
                word = word.capitalize()

            # Then take that list and re-concatenate it's strings back into one string, joined, with
            # no intervening characters between the words.
            #
            # First we specify the joining character, which in this case is nothing.
            s = ""

            # Then join.
            name = s.join(name_ls)

        log = logging.getLogger(f"{PROG_NAME}.{name}")

    # No matter what route we took to define it, return the log object
    return log


def parse_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", type=str, required=True, help="Target domain")
    parser.add_argument(
        "-o", "--output", type=str, required=False, help="Output to file"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        required=False,
        help="Switch the verbose output flag to True",
    )
    return parser.parse_args()


def banner():
    """

    Print program information to console.

    """
    global version

    print("Name: sub-dom-spy")
    print(f"Version: {version}")
    print("Copyright: Taylor-Jayde Blackstone")
    print("License: MIT")
    print("Description: Sub-domain finder.")
    time.sleep(2)


def parse_url(url):
    """

    Parses a given URL

    Args:
        url (str): The URL to parse.

    Returns:
        host: The data parsed from the url.
    """
    log = start_logger(name="ParseURL")
    try:
        log.info(f"Attempting to contact {url}")
        host = urllib3.util.url.parse_url(url).host
    except Exception as e:
        log.exception("[*] Invalid domain, please try again.")
        sys.exit(1)

    return host


def write_subdomains_to_disk(subdomain, output_file):
    log = start_logger(name="WriteSubDomainsToDisk")
    log.debug(f"Received request to write a mined sub-domain to {output_file}")
    with open(output_file, "a") as file:
        file.write(subdomain + "\n")
        file.close()


def main():
    banner()
    subdomains = []

    args = parse_args()

    log = start_logger(verbose=args.verbose)

    target = parse_url(args.domain)
    output = args.output

    req = requests.get(f"https://crt.sh/?q=%.{target}&output=json")

    if not req.status_code == 200:
        log.exception("[!] Something's gone wrong!")
        sys.exit(1)

    for (key, value) in enumerate(req.json()):
        subdomains.append(value["name_value"])

    print(f"\n[*] ****** TARGET: {target} ****** [*] \n")

    subs = sorted(set(subdomains))

    for sub in subs:
        print(f"[*] {sub}\n")
        if output is not None:
            write_subdomains_to_disk(sub, output)

    print("\n\n[>**<] SubDomSpy has completed it's search [>**<]")
    print(f"Found {len(subdomains)} subdomains")


if __name__ == "__main__":
    main()

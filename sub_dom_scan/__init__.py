
PROG_NAME = 'SubDomScan'
AUTHOR = 'Taylor-Jayde Blackstone <t.blackstone@inspyre.tech>'
LICENSE = 'MIT'
DESCRIPTION = 'Scans output files from SubDomSpy scans to see what hosts respond to pings.'
VERSION = 1.0

banner_attrs = [f'Name: {PROG_NAME}', f'Author: {AUTHOR}', f'Version: {VERSION}',
                f'License: {LICENSE}', f'Description: {DESCRIPTION}']


def banner():
    for attr in banner_attrs:
        print(attr)


def parse_args():
    pass


def ping_host(address):
    pass


def main():
    banner()


if __name__ == '__main__':
    main()

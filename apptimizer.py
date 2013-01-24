#!/usr/bin/env python
#
# Main interface to apptimize. Interact with the application thru this script.
#
# Author: Rob Bernabe <rob@rob.pe>
# Github: https://github.com/robbernabe
# Twitter: @rbernabe

import argparse
import sys
from appscript import ApplicationNotFoundError
from apptimize.apptimize import Apptimize
from settings import settings


def process_install(arg_dict):
    print "Handling install"
    # TODO: Check if already installed
    Apptimize.install()


def process_uninstall(arg_dict):
    # TODO: Check if we're installed already, we may not need to do this
    print "Handling uninstall"


def process_application(arg_dict):
    print "Handling application"


def process_network(arg_dict):
    print "Handling network"


def run(arg_dict):
    # TODO: Check DB for what to start/quit! Will need to check the network
    # we're connected to, then see the apps.
    try:
        app = Apptimize(app)
        if app.ready_to_apptimize():
            print "Ready to apptimize!"
            if app.running:
                print "Quitting %s" % app.name
                app.quit()
        else:
            print "Not ready to apptimize..."
            if not app.running:
                print "Opening %s" % app.name
                app.open()
    except ApplicationNotFoundError:
        print 'Application not found: %s' % app


def main():
    """
    Main script to apptimize your Mac.

    """

    # Setup top-level parser then use subparsers
    # http://docs.python.org/dev/library/argparse.html#argparse.ArgumentParser.add_subparsers
    parser = argparse.ArgumentParser(description='apptimize your Mac!')
    subparsers = parser.add_subparsers(dest='commands')

    # Install subparser
    install_parser = subparsers.add_parser('install', help='Installation related tasks')
    install_parser.add_argument('install', action='store_true', default=True, help='Install apptimize on your Mac')
    install_parser.set_defaults(func=process_install)

    # Uninstall subparser
    uninstall_parser = subparsers.add_parser('uninstall', help='Installation related tasks')
    uninstall_parser.add_argument('uninstall', action='store_true', default=True, help='Uninstall apptimize on your Mac')
    uninstall_parser.set_defaults(func=process_uninstall)

    # Applications subparser
    app_parser = subparsers.add_parser('application', help='Application related tasks')
    app_parser.add_argument('application_name', action='store', help='Name of the application to add or remove')
    app_parser.add_argument('--add', action='store_true', help='Add an application to the apptimize database')
    app_parser.add_argument('--remove', action='store_true', help='Remove an application from the apptimize database')
    app_parser.set_defaults(func=process_application)

    # Networks subparser
    net_parser = subparsers.add_parser('network', help='Network related tasks')
    net_parser.add_argument('network_name', action='store', help='The network to perform tasks on')
    net_parser.add_argument('--add', action='store_true', help='Add a network to the apptimize database')
    #
    # TODO: Add support for apptimizer.py network --add-current
    #
    net_parser.add_argument('--add-current', action='store_true', help='Add the current network you are connected to to the apptimize database')
    net_parser.add_argument('--remove', action='store_true', help='Remove a network from the apptimize database')
    net_parser.set_defaults(func=process_network)

    # Run subparser
    run_parser = subparsers.add_parser('run', help='Run apptimize')
    run_parser.set_defaults(func=run)

    args = vars(parser.parse_args())

    # Run the appropriate processing function
    args['func'](args)


if __name__ == '__main__':
    main()

#!/usr/bin/env python
#
# Main interface to apptimize. Interact with the application thru this script.
#
# Author: Rob Bernabe <rob@rob.pe>
# Github: https://github.com/robbernabe
# Twitter: @rbernabe

import sys
import argparse
from appscript import ApplicationNotFoundError
from apptimize.apptimize import Apptimize
from settings import settings
from subprocess import check_output, CalledProcessError


def check_args(dict):
    if 'add_current' in dict:
        option_type = 'network'
        return
    else:
        option_type = 'application'
    if (dict['add'] is False) and (dict['remove'] is False):
        print "You must supply an action for the %s." % option_type
        print "Please use either --add or --remove"
        sys.exit(1)

def process_install(arg_dict):
    print "Handling install"
    # TODO: Check if already installed
    Apptimize.install()


def process_uninstall(arg_dict):
    # TODO: Check if we're installed already, we may not need to do this
    print "Handling uninstall"


def process_application(arg_dict):
    print "Handling application"
    print arg_dict
    check_args(arg_dict)
    if arg_dict['add'] is True:
        print 'Adding application'
        app = Apptimize()
        # Try/catch?
        app.add_application(arg_dict['application_name'])
    else:
        print 'Removing application'

def process_network(arg_dict):
    print "Handling network"
    print arg_dict
    check_args(arg_dict)
    if arg_dict['add'] is True:
        print 'Adding network'
        app = Apptimize()
        # Try/catch?
        app.add_application(arg_dict['application_name'])
    elif arg_dict['add_current'] is True:
        # TODO: Check that we're indeed connected to a network and have
        # internet access
        bssid = str(check_output(settings.BSSID_CMD, shell=True)).strip()
        ssid = str(check_output(settings.SSID_CMD, shell=True)).strip()
        print bssid
        print ssid
        # Add network entry to db
    else:
        print 'Removing application'


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
    install_parser = subparsers.add_parser('install', help='Install apptimize on your Mac')
    install_parser.add_argument('install', action='store_true', default=True, help='Install apptimize on your Mac')
    install_parser.set_defaults(func=process_install)

    # Uninstall subparser
    uninstall_parser = subparsers.add_parser('uninstall', help='Uninstall apptimize from your Mac')
    uninstall_parser.add_argument('uninstall', action='store_true', default=True, help='Uninstall apptimize from your Mac')
    uninstall_parser.set_defaults(func=process_uninstall)

    # Applications subparser
    app_parser = subparsers.add_parser('application', help='Manage applications managed by apptimize')
    app_parser.add_argument('application_name', action='store', help='Name of the application to add or remove')
    app_parser.add_argument('--add', action='store_true', help='Add an application to the apptimize database')
    app_parser.add_argument('--remove', action='store_true', help='Remove an application from the apptimize database')
    app_parser.set_defaults(func=process_application)

    # Networks subparser
    net_parser = subparsers.add_parser('network', help='Manage networks managed by apptimize')
    net_parser.add_argument('network_name', nargs='?', help='The network to perform tasks on')
    net_parser.add_argument('--add', action='store_true', help='Add a network to the apptimize database')
    net_parser.add_argument('--add-current', action='store_true', help='Add the current network you are connected to to the apptimize database')
    net_parser.add_argument('--remove', action='store_true', help='Remove a network from the apptimize database')
    net_parser.set_defaults(func=process_network)

    # Run subparser
    run_parser = subparsers.add_parser('run', help='apptimize your Mac! (not meant to be invoked manually)')
    run_parser.set_defaults(func=run)

    args = vars(parser.parse_args())

    # 'network_name' was an optional argument with nargs='?', so make sure it
    # was provided as an argument to the --add or --remove cases.
    if 'network_name' in args:
        if args['network_name'] is None and ((args['remove'] is False) or (args['add'] is False)):
            if args['add_current'] is False:
                print "You must supply a network name with the --add or --remove options"
                sys.exit(1)

    # Run the appropriate processing function
    args['func'](args)


if __name__ == '__main__':
    main()

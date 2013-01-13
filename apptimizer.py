#!/usr/bin/env python
#
# Quit Dropbox when tethering to iPhone to save bandwidth.
#
# Author: Rob Bernabe <rob@rob.pe>
# Github: https://github.com/robbernabe
# Twitter: @rbernabe

import argparse
from appscript import ApplicationNotFoundError
from apptimize.apptimize import *
from settings import settings


def main():
    """
    Main script to apptimize your Mac.

    Runs only when you are connected to devices you specify in settings to help
    preserve bandwidth (and keep your bill low!).

    """

    parser = argparse.ArgumentParser(description='apptimize your Mac!')
    parser.add_argument('-i', '--install', action='store_true', help='Install apptimize to your system')
    parser.add_argument('-u', '--uninstall', action='store_true', help='Uninstall apptimize from your system')
    parser.add_argument('-a', '--add', action='store_true', help='Add a new network to apptimize')
    parser.add_argument('-r', '--remove', action='store_true', help='Remove a network from apptimize')
    args = vars(parser.parse_args())

    # TODO: Check that we're installed before running without any arguments first (check for plist?)

    arg_count = 0
    for k,v in args.iteritems():
        if v == True:
            arg_count += 1

    if arg_count > 1:
        print 'Error: Only one option allowed at a time!'
        sys.exit(1)

    # At this point we can handle each option individually, since we will not get more than two options
    if args['install']:
        Apptimize.install()
    elif args['uninstall']:
        # TODO: add fucntions here
        print 'uninstall'
    elif args['add']:
        # TODO: add fucntions here
        print 'add'
    elif args['remove']:
        # TODO: add fucntions here
        print 'remove'
    else:
        for app in settings.APP_LIST:
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


if __name__ == '__main__':
    main()

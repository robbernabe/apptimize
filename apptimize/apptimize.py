import sys
import shutil
import appscript
import plistlib
import inspect
from subprocess import check_output, CalledProcessError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import settings
from models import Networks

class Apptimize(object):
    """
    Base class

    """

    def __init__(self, application_name):
        """
        Setup operations.

        """

        self.name = application_name
        self.app_object = appscript.app(self.name)              # appscript object to work with
        self.app_path = self.app_object.AS_appdata.identifier   # absolute path to application

        # Create our database object
        engine = create_engine(settings.DATABASE_URI, echo=True)
        Session = sessionmaker(bind=engine)
        self.db_conn = Session()

        # Get all the networks we have stored already for easy access
        self.all_networks = self.db_conn.query(Networks).all()

        # TODO: Check if there are any networks and set related attributes (num_networks, num_enabled, num_disabled, etc.)

    def running(self):
        """
        Is the app currently running?

        """
        return self.app_object.isrunning()

    def ready_to_apptimize(self):
        """
        Are we connected to any of our designated default gateways?

        """

        gateway_mac = str(check_output(settings.BSSID_CMD, shell=True)).strip()
        print gateway_mac
        print settings.TETHERING_MACS
        if gateway_mac.lower() in settings.TETHERING_MACS:
            return True
        else:
            return False

    def open(self):
        """
        Open an application.

        """

        self.app_object.launch()

    def quit(self):
        """
        Quit an application.

        """

        self.app_object.quit()

    def add_application(self):
        """
        Add an application to the apptimize database.

        """

        pass

    def remove_application(self):
        """
        Remove an application from the apptimize database.

        """

        pass

    def add_network(self):
        """
        Add a network to the apptimize database.

        """

        pass

    def remove_network(self):
        """
        Remove a network from the apptimize database.

        """

        pass

    @staticmethod
    def check_requirements():
        """
        Check that the installing system meets the installation requirements.

        """
        pass

    @staticmethod
    def install():
        """
        Run installation-related procedures.

        """

        # Check installation requirements
        # Apptimize.check_requirements()

        # Install our base system
        try:
            plistlib.writePlist(settings.PLIST_DICT, settings.PLIST_LOCATION)
            check_output('launchctl load %s' % settings.PLIST_LOCATION, shell=True)
            caller_file = inspect.stack()[1]
            shutil.copy(caller_file[1], '/usr/local/bin')
        except IOError as e:
            print 'FATAL: problem installing files: %s' % e
            sys.exit(1)
        except CalledProcessError:
            print 'FATAL: Problem loading plist file into LaunchServices.'
            sys.exit(1)

        # Setup our permanent storage (SQLite database)
        try:
            from models import Base
            # TODO: if file exists, rename it before creating new
            # Turn echo off to disable debug info
            engine = create_engine(settings.DATABASE_URI, echo=True)
            Base.metadata.create_all(engine)
        except Exception as e:
            print 'Fatal: Problem installing sqlite database: %s' % e

    @staticmethod
    def uninstall():
        """
        Remove apptimize from your system.

        """

        # TODO: unload plist, remove plist, remove script
        pass

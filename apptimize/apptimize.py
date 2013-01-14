import sys
import shutil
import appscript
import plistlib
import inspect
import datetime
from subprocess import check_output, CalledProcessError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import settings
from models import Networks, Applications


class Apptimize(object):
    """
    Base class

    """

    def __init__(self, application_name):
        """
        Setup operations.

        """

        self.app_name = application_name
        self.app_object = appscript.app(self.app_name)              # appscript object to work with
        self.app_path = self.app_object.AS_appdata.identifier   # absolute path to application
        self.network_dict = {}

        # Create our database object
        engine = create_engine(settings.DATABASE_URI, echo=False)
        Session = sessionmaker(bind=engine)
        self.db = Session()

        # Get all the networks we have stored already for easy access
        # self.all_networks = self.db.query(Networks).all()
        # self.app_applications = self.db.query(Applications).all()

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

    @staticmethod
    def add_application(apptimize_object):
        """
        Add an application to the apptimize database.

        """

        now = datetime.datetime.now()
        app_name = apptimize_object.app_name
        app_path = apptimize_object.app_path

        # TODO: try/catch
        application = Applications(app_name, app_path, now, enabled=True)
        apptimize_object.db.add(application)
        apptimize_object.db.commit()

    @staticmethod
    def remove_application(apptimize_object):
        """
        Remove an application from the apptimize database.

        """

        pass

    @staticmethod
    def add_network(apptimize_object):
        """
        Add a network to the apptimize database.

        network_dict = {
            'bssid': 'bssid_here',
            'ssid': 'ssid_here'
        }

        """

        now = datetime.datetime.now()

        # TODO: try/catch
        network = Networks(
            apptimize_object.network_dict['bssid'],
            apptimize_object.network_dict['ssid'],
            now,
            enabled=True
        )
        apptimize_object.db.add(network)
        apptimize_object.db.commit()

    @staticmethod
    def remove_network(apptimize_object):
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
            engine = create_engine(settings.DATABASE_URI, echo=False)
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

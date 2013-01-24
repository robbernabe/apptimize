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

    def __init__(self):
        """
        Setup operations.

        """

        self.app_name = None
        self.app_object = None
        self.app_path = None
        self.net_bssid = None
        self.net_ssid = None

        # Create our database object
        engine = create_engine(settings.DATABASE_URI, echo=False)
        Session = sessionmaker(bind=engine)
        self.db = Session()

        # TODO: Check that a database exists when we're called. Otherwise,
        # we'll need to reinstall.

        # Get all the networks & apps we have stored already for easy access
        self.all_networks = self.db.query(Networks).all()
        self.all_applications = self.db.query(Applications).all()

        # TODO: Check if there are any networks and set related attributes
        # (num_networks, num_enabled, num_disabled, etc.)

    def running(self):
        """
        Is the app currently running?

        """
        return self.app_object.isrunning()

    def ready_to_apptimize(self):
        """
        Are we connected to any of our designated networks?

        """

        str = str(check_output(settings.BSSID_CMD, shell=True)).strip()
        if str.lower() in settings.TETHERING_MACS:
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

    def add_application(self, application_name):
        """
        Add an application to the apptimize database.

        """

        self.app_name = application_name
        self.app_object = appscript.app(self.app_name)              # appscript object to work with
        self.app_path = self.app_object.AS_appdata.identifier   # absolute path to application
        now = datetime.datetime.now()

        # TODO: try/catch
        application = Applications(self.app_name, self.app_path, now, enabled=True)
        self.db.add(application)
        self.db.commit()

    def remove_application(self):
        """
        Remove an application from the apptimize database.

        """

        pass

    def add_network(self, network_dict):
        """
        Add a network to the apptimize database.

        network_dict = {
            'bssid': 'bssid_here',
            'ssid': 'ssid_here'
        }

        """

        # TODO: validate network_dict

        for key, value in network_dict.iteritems():
            if key == 'bssid':
                self.net_bssid = value
            elif key == 'ssid':
                self.net_ssid = value

        now = datetime.datetime.now()

        # TODO: try/catch
        network = Networks(
            self.net_bssid,
            self.net_ssid,
            now,
            enabled=True
        )
        self.db.add(network)
        self.db.commit()

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
        # TODO: Apptimize.check_requirements()

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
            print 'FATAL: Problem loading plist file into LaunchServices'
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

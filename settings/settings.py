import os

(dbpath, tail) = os.path.split(os.path.dirname(os.path.abspath(__file__)))
home = os.environ.get('HOME')
DATABASE_URI = 'sqlite:///%s/db/networks.sql3' % dbpath

# The list of applications you want to apptimize when tethering to your mobile device
# NOTE: You can add multiple applications here
APP_LIST = (
    'Dropbox',
)

# The tuple of MAC addresses of mobile devices
# NOTE: You can add multiple devices here
TETHERING_MACS = (
    'bc:3b:af:25:86:a0',    # iPhone
)

AIRPORT_CMD = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I'
BSSID_CMD = '%s | grep BSSID | awk \'{print $2}\'' % AIRPORT_CMD
SSID_CMD = '%s | grep [^B]SSID | cut -f2 -d\: | sed \'s/[ ]*//\'' % AIRPORT_CMD

PLIST_LOCATION = '%s/Library/LaunchAgents/Apptimize.plist' % home
PLIST_DICT = {
    'Label': 'rob.pe.apptimize',
    'ProgramArguments': ['/usr/local/bin/apptimizer.py'],
    'WatchPaths': ['/Library/Preferences/SystemConfiguration']
}

## User Story

* As a user, I want to be able to not have certain applications run when Im connected to
  specific networks (wired or wireless). For example, when tethered to my
iPhone, I would prefer to not have my teams' Dropbox syncing constantly using my
my data plan. Therefore, I'd like Dropbox to quit automatically when Im
connected to my iPhone, and automatically start when Im back on a different
network.
* I should be able to add/remove a network to the app by running a command when connected to that
  network

        ./apptimizer.py --network --add
        ./apptimizer.py --network --remove

* I should be able to add an application to the app (by name) by running a
  command when connected to the network

        ./apptimizer.py --application --add Dropbox
        ./apptimizer.py --application --remove Dropbox

* I should be able to list all the networks/applications that we've installed

        ./apptimizer.py --application --list
        ./apptimizer.py --network --list

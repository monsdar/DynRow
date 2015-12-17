import sys
import dynrow_args

import logbook

from UI.PyGameUi import PyGameUi
from Boats.BoatConcept2 import BoatConcept2
from Logic.Playground import Playground
import managers

from ErgStatsFactory import ErgStats

log = logbook.Logger("DynRow")

DELTAT = 16  # run with ~60FPS


manager = None
playground = Playground()  # the playground is a class which holds all the information (all the boats etc)
ui = PyGameUi() # the UI which will display the playground on a graphical interface


def gameLoop():
    log.debug(" ")
    log.debug("gameloop start")
    #check if the workout is active
    isWorkoutActive = ErgStats.isWorkoutActive()
    if not isWorkoutActive:
        ErgStats.resetStatistics()
        playground.reset()
    else:
        #update the ergometer data
        log.debug("gameloop about to call ErgStats.update")
        ErgStats.update()

    manager.update(ErgStats)
    log.debug("about to playground.update(%s)"%ErgStats.time)
    playground.update(ErgStats.time)
    ui.update(playground)

    #display the message after the UI has been rendered
    if not isWorkoutActive:
        ui.showMessage("Please start rowing...")

    log.debug("gameloop end")



def main():

    global manager

    # init the player boat
    player = BoatConcept2(dynrow_args.args.name)
    playground.setPlayerBoat(player)

    
    if dynrow_args.args.dointervals:
        manager = managers.IntervalManager(playground.storage)
    else:
        manager = managers.StandardManager(playground.storage)

    manager.initialize(playground)

    # Init the Concept2
    ErgStats.connectToErg()

    #init the UI, register the GameLoop and run it
    ui.registerCallback(gameLoop)
    ui.setCycleTime(DELTAT)
    ui.run()

#log_handler = logbook.StreamHandler(sys.stdout, level=dynrow_args.args.loglevel)
log_handler = logbook.StreamHandler(open("dynrow.log", "w"), level=dynrow_args.args.loglevel)
if __name__ == "__main__":
    with log_handler.applicationbound():
        main()


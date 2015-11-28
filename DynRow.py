
import glob
import os, sys
import dynrow_args

import logbook

from UI.PyGameUi import PyGameUi
from Boats.BoatConcept2 import BoatConcept2
from Boats.BoatBoomerang import BoatBoomerang
from Boats.BoatGhost import BoatGhost
from Boats.BoatConstant import BoatConstant
from Logic.Playground import Playground


from ErgStatsFactory import ErgStats

log = logbook.Logger("DynRow")

DELTAT = 16  # run with ~60FPS

#get newest workout file
#do this before the Playground gets created (thus creating a new Ghostfile)
ghostFiles = glob.glob('*.db')
if len(ghostFiles) > 0:
    newestGhost = max(ghostFiles, key=os.path.getctime)
else:
    newestGhost = ""

playground = Playground()  # the playground is a class which holds all the information (all the boats etc)
ui = PyGameUi() # the UI which will display the playground on a graphical interface


def gameLoop():
    #check if the workout is active
    isWorkoutActive = ErgStats.isWorkoutActive()
    log.debug("gameloop() isWorkoutActive=%s"%isWorkoutActive)
    if not isWorkoutActive:
        ErgStats.resetStatistics()
        playground.reset()
    else:
        #update the ergometer data
        log.debug("gameloop about to call ErgStats.update")
        ErgStats.update()

    log.debug("about to playground.update(%s)"%ErgStats.time)
    playground.update(ErgStats.time)
    ui.update(playground)

    #display the message after the UI has been rendered
    if not isWorkoutActive:
        ui.showMessage("Please start rowing...")



def main():
    # init the player boat
    player = BoatConcept2(dynrow_args.args.name)
    playground.setPlayerBoat(player)

    #init the AI boats
    playground.addBoat(BoatBoomerang("Pacer", 130, 24, 50, 4))
    playground.addBoat(BoatBoomerang("Other Pacer", 129, 25, 2))
    playground.addBoat(BoatConstant("Steady", 129, 24))

    if not newestGhost == "":
        playground.addBoat(BoatGhost("Ghost", newestGhost))

    # Init the Concept2
    ErgStats.connectToErg()

    #init the UI, register the GameLoop and run it
    ui.registerCallback(gameLoop)
    ui.setCycleTime(DELTAT)
    ui.run()

log_handler = logbook.StreamHandler(sys.stdout, level=dynrow_args.args.loglevel)
if __name__ == "__main__":
    with log_handler.applicationbound():
        main()


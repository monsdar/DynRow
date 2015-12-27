import logbook

import glob, os

from Boats.BoatBoomerang import BoatBoomerang
from Boats.BoatConstant import BoatConstant
from Boats.BoatGhost import BoatGhost



log = logbook.Logger("StandardManager")

class StandardManager(object):

    def __init__(self, storage):
        pass

    def initialize(self, playground):
        log.debug("initializing standard manager")

        #init the AI boats
        playground.addBoat(BoatBoomerang("Pacer", 140, 25, 30, 4))
        playground.addBoat(BoatBoomerang("Other Pacer", 140, 24, 15, 4))
        playground.addBoat(BoatConstant("Steady", 136, 25))

        #get newest workout file
        #do this before the Playground gets created (thus creating a new Ghostfile)
        ghostFiles = glob.glob('*.db')
        if len(ghostFiles) > 0:
            newestGhost = max(ghostFiles, key=os.path.getctime)
        else:
            newestGhost = "" 
        if not newestGhost == "":
            playground.addBoat(BoatGhost("Ghost", newestGhost)) 

    def update(self, ergstats):
        pass

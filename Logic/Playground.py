import logbook
from Storage.SQLiteStorage import SQLiteStorage
from ErgStatsFactory import ErgStats


log = logbook.Logger("Playground")


class Playground():
    def __init__(self):
        self.boats = []
        self.position = 0.0
        self.storage = SQLiteStorage() #needed to store the current workout to file (needed for ghosting)
        self._pause_boats = False

    def removeNonPlayerBoats(self):
        self.boats = []

    def pauseBoats(self):
        self._pause_boats=True

    def unPauseBoats(self):
        self._pause_boats=False

    def getCurrentPosition(self):
        return self.position
    
    def addBoat(self, boat):
        self.boats.append(boat)
        
    def getBoats(self):
        return self.boats
        
    def getPlayerBoat(self):
        return self.playerBoat
        
    def setPlayerBoat(self, boat):
        self.playerBoat = boat

    def reset(self):
        for boat in self.boats:
            boat.reset()
        self.playerBoat.reset()

    def update(self, timeGone):
        log.debug("update(%s) _pause_boats=%s"%(timeGone, self._pause_boats))
        if not self._pause_boats:
            #move all the bots
            for boat in self.boats:
                boat.move(timeGone)
            #move the player
            self.playerBoat.move(timeGone)
        else:
            log.debug("did not move the boats")

        #store the current state into the storage if not in a transition period
        if ErgStats.workout_state not in (3,6,7,8,9) and not ( timeGone==0 and ErgStats.distance > 1):  # TODO: refactor constants out of IntervalManager and use them here 
            # the timeGone / distance check is to avoid writing a race condition into the storage where the time is 0 and the distance is 100
            self.storage.storeState(timeGone)

import time

import logbook
log = logbook.Logger("BoatConcept2")

from Logic.Boat import Boat
from ErgStatsFactory import ErgStats

class BoatConcept2(Boat):
    def __init__(self, name, distance=0):
        super(BoatConcept2, self).__init__(name, distance)

    def initialize(self):
        pass

    def move(self, timeGone):
        self.distance = ErgStats.distance
        self.pace = ErgStats.pace
        log.debug("BoatConcept2.move(%s): distance now:%s pace now:%s"%(timeGone, self.distance, self.pace))

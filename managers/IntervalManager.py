"""
Manage a series of interval races.  Each interval afer the first adds a ghost boat that rows the previous n intervals.

interval #:
0 create a single 'ghost' boat 
        TODO: later add average pace boat
1..N:  add boats for successive intervals 

at (end of interval/n seconds before rest):
    reset playground
    remove non player boats
    add new ghost boats
    do 'start rowing' thing


TODO:
    . add erg state update to im
    . add im reset everuthong at end of interval

(C) 2015 Kevin Dahlhausen

"""
import logbook

import Boats

log = logbook.Logger("IntervalManager")


class IntervalManager(object):

    def __init__(self, storage):
        self.current_interval = 0
        self.max_number_of_interval_ghosts = 3
        self.storage = storage


    def initialize(self, playground):
        log.debug("initializing interval manager")
        playground.addBoat(Boats.BoatConstant.BoatConstant("Steady", 136, 25))


    def initialize_for_interval(self, interval_number):
        "intialize playground for intervals after the first"

        self.playground.removeNonPlayerBoats()
        self.playground.reset()

        # interval_number is 1 during rest period of first interval
        for previous_interval_number in range(0, interval_number):
            name = "Interval %d"%previous_interval_number
            boat = Boats.BoatGhost.BoatGhost(name, interval=previous_interval_number, storage=self.storage)
            self.playground.addBoat(boat)


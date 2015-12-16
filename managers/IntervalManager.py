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

WS_WAITING_TO_BEGIN=0
WS_REST_INTERVAL=3
WS_TIMED_INTERVAL_WORK=4
WS_DIST_INTERVAL_WORK=5
WS_REST_END_TO_TIME_WORK=6
WS_REST_END_TO_DIST_WORK=7
WS_TIME_WORK_END_TO_REST=8
WS_DIST_WORK_END_TO_REST=9


class IntervalManager(object):

    def __init__(self, storage):
        self.current_interval = 0
        self.max_number_of_interval_ghosts = 3
        self.storage = storage
        self.previous_state=WS_WAITING_TO_BEGIN
        self.has_reset_for_next_interval=False


    def initialize(self, playground):
        log.debug("initializing interval manager")
        playground.addBoat(Boats.BoatConstant.BoatConstant("Steady", 136, 25))


    def update(self, ErgStats):
        # stop boats moving at end of work interval 
        if self.previous_state in (WS_TIMED_INTERVAL_WORK, WS_DIST_INTERVAL_WORK) and \
           ErgStats.workout_state in (WS_REST_INTERVAL, WS_TIME_WORK_END_TO_REST, WS_DIST_WORK_END_TO_REST):
            # work segment just finished, pause the boats
            self.playground.pauseBoats()

        elif ErgStats.workout_state==WS_REST_INTERVAL and ErgStats.rest_time_remaining==4 and not self.has_reset_for_next_interval:
            # reset the field for the next interval but leave boats paused -- might need to update playground reset
            self.playground.reset()
            self.initialize_for_interval(ErgStats.interval_count)
            self.has_reset_for_next_interval=True

        elif self.previous_state in (WS_REST_INTERVAL, WS_REST_END_TO_TIME_WORK, WS_REST_END_TO_DIST_WORK) and \
                ErgStats.workout_state in (WS_TIMED_INTERVAL_WORK, WS_DIST_INTERVAL_WORK): 
            # let boats move, just started a new interval
            self.has_reset_for_next_interval=False
            self.playground.unPauseBoats()
        self.previous_state = ErgStats.workout_state



    def initialize_for_interval(self, interval_number):
        "intialize playground for intervals after the first"

        self.playground.removeNonPlayerBoats()
        self.playground.reset()

        # interval_number is 1 during rest period of first interval
        for previous_interval_number in range(0, interval_number):
            name = "Interval %d"%previous_interval_number
            boat = Boats.BoatGhost.BoatGhost(name, interval=previous_interval_number, storage=self.storage)
            self.playground.addBoat(boat)


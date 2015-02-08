import math
from Logic.Boat import Boat
from PyRow.ErgStats import ErgStats

class BoatRubberband(Boat):
    def __init__(self, name, pace=150, spm=20, rubberDistance=50, distance=0):
        Boat.__init__(self, name, distance)
        self.pace = pace            #time in seconds the boat needs to row 500m
        self.spm = spm              #strokes per minute
        self.rubberDistance = rubberDistance #the distance to the player at which rubberbanding begins
        self.amplitude = 0.1       #amplitude with which the boats are rowing

        self.offsetTime = 0.0 #needed if the boat changes its pace
        self.offsetDist = 0.0 #needed if the boat changes its pace
        self.currentTime = 0.0#needed if the boat changes its pace

    def changePace(self, newPace):
        self.pace = newPace
        self.offsetTime = self.currentTime
        self.offsetDist = self.distance

    def move(self, timeGone):
        #if the boat is out of the given distance change the pace to the player pace
        distToPlayer = abs(self.distance - ErgStats.distance)
        if(distToPlayer > self.rubberDistance and not ErgStats.pace == self.pace ):
            self.changePace(ErgStats.pace)

        self.currentTime = timeGone
        strokesPerSecond = self.spm / 60.0
        velocity = 500.0 / self.pace

        timeGoneMs = ((timeGone - self.offsetTime) / 1000.0) #time is given in milliseconds, we need seconds
        timeCalc = timeGoneMs + self.amplitude * -math.sin(timeGoneMs * strokesPerSecond * 2.0 * math.pi)
        self.distance = self.offsetDist + (velocity * timeCalc)
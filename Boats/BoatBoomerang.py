import math
from Logic.Boat import Boat
from ErgStatsFactory import ErgStats


class BoatBoomerang(Boat):

    def __init__(self, name, pace=150, spm=20, boomerDistance=50, distance=0):
        super(BoatBoomerang, self).__init__(name, distance)
        self.pace = pace            #time in seconds the boat needs to row 500m
        self.originalPace = pace    #do not forget the original pace
        self.spm = spm              #strokes per minute
        self.amplitude = 0.1       #amplitude with which the boats are rowing

        self.boomerDistance = boomerDistance #the distance to the player at which the boomerang activates
        self.boost = boost #the speedboost which the boat will get when out of boomerDistance
        self.lastSecCheck = 0 #the last second where we checked the speed

        self.offsetTime = 0.0 #needed if the boat changes its pace
        self.offsetDist = 0.0 #needed if the boat changes its pace
        self.currentTime = 0.0#needed if the boat changes its pace

    def reset(self):
        super(BoatBoomerang, self).reset()
        self.pace = self.originalPace
        self.lastSecCheck = 0
        self.offsetTime = 0.0
        self.offsetDist = 0.0
        self.currentTime = 0.0

    def changePace(self, newPace):
        self.pace = newPace
        self.offsetTime = self.currentTime
        self.offsetDist = self.distance

    def move(self, timeGone):
        #check once a second if we need to change the pace
        currentSec = int((timeGone) % 10)
        if( currentSec != self.lastSecCheck ):
            #if the boat is out of the given distance change the pace get back to the player
            distToPlayer = self.distance - ErgStats.distance

            if(distToPlayer > self.boomerDistance and (not self.pace >= ErgStats.pace) ):
                self.changePace(ErgStats.pace + 5.0) #check if we need to row slower
            elif(distToPlayer < -self.boomerDistance and (not self.pace <= ErgStats.pace) ):
                self.changePace(ErgStats.pace - 5.0) #or faster
            elif((distToPlayer <= 1.0) and (distToPlayer >= -1.0) and (not self.pace == self.originalPace)):
                self.changePace(self.originalPace) #or get back to the original pace
            self.lastSecCheck = currentSec

        self.currentTime = timeGone
        strokesPerSecond = self.spm / 60.0
        velocity = 500.0 / self.pace

        timeGoneOffset = (timeGone - self.offsetTime) #calc the offset onto the time
        timeCalc = timeGoneOffset + self.amplitude * -math.sin(timeGoneOffset * strokesPerSecond * 2.0 * math.pi)
        self.distance = self.offsetDist + (velocity * timeCalc)

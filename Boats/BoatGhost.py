
from Logic.Boat import Boat
from Storage.SQLiteStorage import SQLiteStorage

class BoatGhost(Boat):
    def __init__(self, name, filename=None, distance=0, interval=0, storage=None):
        Boat.__init__(self, name, distance)
        if storage is not None:
            self.storage=storage
        else:
            self.storage = SQLiteStorage(filename)
        self.interval=interval

    def reset(self):
        pass

    def move(self, timeGone):
        data = self.storage.getDataTuple(timeGone, interval)
        if not data == None:
            self.distance = data[0]
            self.pace = data[2]

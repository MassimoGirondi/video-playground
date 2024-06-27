import datetime as dt
class TimeTracker():

    def __init__(self):
        self.times = {}
        self.last = dt.datetime.now()

    def __setitem__(self, key, value):
        if key in self.times:
            self.times[key].append(value)
        else:
            self.times[key] = [value]


    def __iter__(self):
        return iter(self.itemlist)
    def keys(self):
        return self.itemlist
    def values(self):
        return [self[key] for key in self]
    def itervalues(self):
        return (self[key] for key in self)
    def __repr__(self):

        avg = {k: (sum(v) / len(v) if len(v) else 0) for k,v in self.times.items() }
        s = ", ".join([f"{k}: {v}" for k,v in avg.items()])
        return s

    def reset(self):
        for k in self.times:
            self.times[k] = []

    def start(self):
        self.last= dt.datetime.now()
    def store(self, key):
        now = dt.datetime.now()
        t = now - self.last 
        self[key] = t.seconds*1e6 + t.microseconds

    def step(self, key):
        self.store(key)
        self.start()

instance = None
def get():
    global instance
    if not instance:
        print("Creating a new Time Tracker")
        instance = TimeTracker()
    return instance

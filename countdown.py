"""
A countdown exercise using Twisted. See http://krondo.com/?p=1333
"""

from twisted.internet import reactor
from twisted.internet.task import LoopingCall

class Countdown(object):
    """Counts down from start to 0 with a given delay at each step.
    """
    def __init__(self, start=5, delay=1):
        self.counter = start
        self.delay = delay
        self.done = False

    def count(self):
        if self.counter == 0:
            self.done = True
        else:
            print self.counter, '...'
            self.counter -= 1
            reactor.callLater(self.delay, self.count)

class CountdownManager(object):
    """
    Keeps track of a list of counters, stopping the reactor when they all 
    reach 0.
    """
    def __init__(self, countdowns=[]):
        self.countdowns = countdowns
        self.checker = LoopingCall(self.check_all_counters)

    def add(self, countdown):
        self.countdowns.append(countdown)

    def start(self):
        self.check_if_done()
        self.checker.start(0)
        for c in self.countdowns:
            c.count()

    def check_if_done(self):
        if not self.countdowns:
            reactor.stop()

    def check_all_counters(self):
        for c in self.countdowns:
            if c.done:
                self.countdowns.remove(c)
            self.check_if_done()

if __name__ == '__main__':
    manager = CountdownManager()

    for i in range(1, 4):
        manager.add(Countdown(delay=i))

    reactor.callWhenRunning(manager.start)

    print 'Start!'
    reactor.run()
    print 'Stop!'

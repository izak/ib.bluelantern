import os
import logging
from threading import Lock
from csv import writer as csvwriter
from collections import deque, namedtuple
from ib.bluelantern.event import MetricReceived

logger = logging.getLogger(__name__)

class SlidingWindow(object):
    def __init__(self, interval):
        self.interval = interval
        self.queue = deque()

    def append(self, ts, x):
        t = ts - self.interval
        while len(self.queue) > 0 and self.queue[0][0] < t:
            self.queue.popleft()
        self.queue.append((ts, x))

    def average(self):
        return self.sum()/len(self.queue)

    def sum(self):
        return sum([y for x, y in self.queue])

    def min(self):
        return min([y for x, y in self.queue])

    def max(self):
        return max([y for x, y in self.queue])

def make_treatments(window):
    return {
        'avg': window.average,
        'min': window.min,
        'max': window.max,
        'sum': window.sum
    }

class Structure(object):
    def __init__(self, window, treatment):
        self.window = window
        treatments = make_treatments(window)
        self.treat = treatments.get(treatment, None)
        self.ts = 0

    def record(self, ts, x):
        self.window.append(ts, x)

def parse_cfg(cfg):
    a, b = cfg.strip().split(' ')[:2]
    name, interval = a.split('@')
    interval = int(interval)

    columns = [c.split(':')[:2] for c in b.split(',')]
    columns = {x: Structure(SlidingWindow(interval), y) for x, y in columns}

    Config = namedtuple("Config", "name interval columns")
    return Config(name, interval, columns)

def factory(filename, cfg):
    # TODO use cfg to set up columns
    fp = open(filename, 'a')
    writer = csvwriter(fp)

    def handler(event):
        if event.name != cfg.name:
            return # Not the droid we're looking for

        # If it is the equipment we're looking for, see if any
        # if we need to record a value for a column
        try:
            for column, structure in cfg.columns.items():
                if column != event.unit:
                    continue
                structure.record(event.timestamp, event.value)

                if structure.ts == 0: # First time
                    structure.ts = event.timestamp
                    continue
                if structure.ts >= event.timestamp - cfg.interval: # Not time yet
                    continue

                if structure.treat is not None:
                    value = structure.treat()
                else:
                    value = event.value
                writer.writerow([event.timestamp, column, value])
                structure.ts = event.timestamp
            fp.flush()
        except Exception, e:
            logger.error(str(e))
    return handler

def statistics(settings):
    # unit to track (volts, amps, watts, watt-hour, amp-hour)
    # full list: voltage, current, power, energy
    # Interval (how often to log)
    # treatment (avg, min max, sum, none)
    #
    # Format: name@interval unit:treatment[,unit:treatment ...]
    #
    # example: Log volts and amps from equipment named `mppt` to file
    # Victron_MPPT_75_15, every two minutes, no treatment
    # csvlog.statistic.Victron_MPPT_75_15 = mppt@120 v:none,a:none
    #
    # Log watt hours, every 5 minutes, total produced
    # csvlog.statistic.production = mppt wh:sum@300
    prefix = 'csvlog.statistic.'
    options = dict(
        (key[len(prefix):], settings[key])
        for key in settings if key.startswith(prefix))
    return options


def includeme(config):
    stats = statistics(config.registry.settings)
    d = config.registry.settings.get('csvlog.directory')
    for filename, cfg in stats.items():
        handler = factory(os.path.join(d, filename)+'.csv', parse_cfg(cfg))
    config.add_subscriber(handler, MetricReceived)

import logging
from threading import Lock
from csv import writer as csvwriter
from ib.bluelantern.event import MetricReceived

logger = logging.getLogger(__name__)

def factory(filename):
    lock = Lock()
    fp = open(filename, 'a')
    writer = csvwriter(fp)
    def handler(event):
        try:
            with lock:
                writer.writerow([event.timestamp, event.instance, event.name, event.type, event.unit, event.value])
                fp.flush()
        except Exception, e:
            logger.error(str(e))
    return handler

def includeme(config):
    handler = factory(
        config.registry.settings.get('csvlog.filename'))
    config.add_subscriber(handler, MetricReceived)

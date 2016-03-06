class MetricReceived(object):
    """ Event fired when a metric arrives from the mqtt broker. """
    def __init__(self, instance, name, timestamp, unit, value):
        self.instance = instance
        self.name = name
        self.timestamp = timestamp
        self.unit = unit
        self.value = value

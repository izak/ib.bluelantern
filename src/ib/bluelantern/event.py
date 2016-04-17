class MetricReceived(object):
    """ Event fired when a metric arrives from the mqtt broker. """
    def __init__(self, instance, name, type, timestamp, unit, value):
        self.instance = instance
        self.name = name
        self.type = type
        self.timestamp = timestamp
        self.unit = unit
        self.value = value

class ChargeMetricReceived(MetricReceived):
    """ Sent when incoming charge is detected. """

class DischargeMetricReceived(MetricReceived):
    """ Sent when outgoing charge is detected. """

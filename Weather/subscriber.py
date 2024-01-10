import sys, traceback, Ice, IceStorm
Ice.loadSlice('WeatherMonitor.ice', ['-I' '/usr/share/slice'])
import Demo

class MonitorI (Demo.Monitor):
    def report (self, measurement, current):
        # Process the measurement...
        print('Obtaining a new measurement')

class Subscriber (Ice.Application):
    def run (self, argv):
        self.shutdownOnInterrupt()
        properties = self.communicator().getProperties()
        proxy = properties.getProperty('IceStorm.TopicManager.Proxy')
        obj = self.communicator().stringToProxy(proxy)
        topicManager = IceStorm.TopicManagerPrx.checkedCast(obj)
        adapter = self.communicator().createObjectAdapter('MonitorAdapter')
        monitorPrx = adapter.addWithUUID(MonitorI())
        try:
            topic = topicManager.retrieve('Weather')
            topic.subscribe(None, monitorPrx)
        except IceStorm.NoSuchTopic:
            # Process error...
            print('Topic not found!')
        adapter.activate()
        self.communicator().waitForShutdown()
        topic.unsubscribe(monitorPrx)
        return 0
    
Subscriber().main(sys.argv, 'subscriber.cfg')
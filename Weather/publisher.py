import sys, traceback, time, Ice, IceStorm
Ice.loadSlice('WeatherMonitor.ice', ['-I' '/usr/share/slice'])
import Demo
class Publisher (Ice.Application):
    def run (self, argv):
        self.shutdownOnInterrupt()
        properties = self.communicator().getProperties()
        proxy = properties.getProperty('IceStorm.TopicManager.Proxy')
        obj = self.communicator().stringToProxy(proxy)
        topicManager = IceStorm.TopicManagerPrx.checkedCast(obj)
        try:
            topic = topicManager.retrieve('Weather')
        except IceStorm.NoSuchTopic:
            topic = topicManager.create('Weather')
            
        pub = topic.getPublisher()
        if (pub.ice_isDatagram()):
            pub = pub.ice_oneway()
        monitor = Demo.MonitorPrx.uncheckedCast(pub)
        for i in range (1, 10):
            m = Demo.Measurement()
            # Get the measurement...
            monitor.report(m)
            time.sleep(1)
        self.communicator().waitForShutdown()
        return 0
    
Publisher().main(sys.argv, 'publisher.cfg')
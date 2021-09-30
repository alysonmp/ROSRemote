import websocket
import threading
import json
import logging
import time
import rospy


class Spacebrew(object):

    # Define any runtime errors we'll need
    class ConfigurationError(Exception):
        def __init__(self, brew, explanation):
            self.brew = brew
            self.explanation = explanation

        def __str__(self):
            return repr(self.explanation)

    class Slot(object):
        def __init__(self, name, brewType, default=None):
            self.name = name
            self.type = brewType
            self.value = None
            self.default = default

        def makeConfig(self):
            print("the name is: " + str(self.name))
            print("the type is: " + str(self.type))
            print("the default is: " + str(self.default))
            d = {'name': self.name, 'type': self.type, 'default': self.default}
            return d

    class Publisher(Slot):
        pass

    class Subscriber(Slot):
        def __init__(self, name, brewType, default=None):
            super(Spacebrew.Subscriber, self).__init__(name, brewType, default)
            self.callbacks = []

        def subscribe(self, target):
            self.callbacks.append(target)

        def unsubscribe(self, target):
            self.callbacks.remove(target)

        def disseminate(self, value):
            for target in self.callbacks:
                target(value)

    def __init__(self, name, description="", server="sandbox.spacebrew.cc", port=9090):
        rospy.loginfo("initialising spacebrew function")
        self.server = server
        self.port = port
        self.name = name
        self.description = description
        self.connected = False
        self.started = False
        self.publishers = {}
        print("the length of publsihers is: " +
              str(len(self.publishers.values())))
        self.subscribers = {}
        self.ws = None
        self.HOST = None

    def addPublisher(self, name, brewType="string", default=None):
        if self.connected:
            raise ConfigurationError(
                self, "Can not add a new publisher to a running Spacebrew instance (yet).")
        else:
            self.publishers[name] = self.Publisher(name, brewType, default)

    def addSubscriber(self, name, brewType="string", default=None):
        if self.connected:
            raise ConfigurationError(
                self, "Can not add a new subscriber to a running Spacebrew instance (yet).")
        else:
            self.subscribers[name] = self.Subscriber(name, brewType, default)

    def makeConfig(self):
        print('inside make config')
        subs = map(lambda x: x.makeConfig(), self.subscribers.values())
        print('Finished subs')
        pubs = map(lambda x: x.makeConfig(), self.publishers.values())

        print("the length of publsihers is: " +
              str(len(self.publishers.values())))
        count = 0
        publisher_string = ''
        for key, value in self.publishers.items():
            count += 1
            if count == len(self.publishers.values()):
                publisher_string += str(value.makeConfig())
            else:
                publisher_string += str(value.makeConfig()) + ', '
            print("Publisher consists of: {}".format(key))

        print("The string is: " + publisher_string)
        # print('Finished pubs')
        # print("The pubs is: {}".format(
        #     list(pubs)))
        # print("The pubs size: {}".format(
        #     type([{'name': 'ROS_Publisher', 'type': 'string', 'default': None}])))

        # print("[{'name': 'ROS_Publisher', 'type': 'string', 'default': None}]")
        # print("yolo: {}".format(list(pubs)))
        # print("The pubs is: {}, of size: {}".format(
        #     list(pubs), type(list(pubs))))
        # TODO: do not print list(pubs), it somehow erases the value
        d = {'config': {
            'name': self.name,
            'description': self.description,
            'publish': {'messages': list(pubs)},
            'subscribe': {'messages': list(subs)},
        }
        }
        print('finished everything returning out of makeConfig function: ')
        return d

    def on_open(self, ws):
        rospy.loginfo("Opennninging brew")
        logging.info("Opening brew.")
        rospy.logwarn("hello")
        result = json.dumps(self.makeConfig())
        rospy.logwarn("hello")
        print(result)
        self.connected = True
        rospy.logwarn("hello2")
        ws.send(result)
        rospy.logwarn("self connected is changed to true: " + result)

    def on_message(self, ws, message):
        msg = json.loads(message)['message']
        sub = self.subscribers[msg['name']]
        sub.disseminate(msg['value'])

    def on_error(self, ws, error):
        logging.error("[on_error] ERROdndndndnR: {0}".format(error))
        logging.error("[on_error] self started " + str(self.started))
        self.on_close(ws)

    def on_close(self, ws):
        print("being asked to close")
        self.connected = False
        while self.started and not self.connected:
            time.sleep(5)
            self.run()

    def publish(self, name, value):
        publisher = self.publishers[name]
        message = {'message': {
            'clientName': self.name,
            'name': publisher.name,
            'type': publisher.type,
            'value': value}}
        self.ws.send(json.dumps(message))

    def subscribe(self, name, target):
        subscriber = self.subscribers[name]
        subscriber.subscribe(target)

    def run(self):
        self.HOST = "ws://" + str(self.server) + ":" + str(self.port)
        self.HOST = "ws://" + str(self.server)

        # print("inside the run function. Trying to connect to: "+ "ws://{0}:{1}".format(self.server, self.port))
        print("inside the run function. Trying to connect to: " + self.HOST)

        # self.ws = websocket.WebSocketApp("ws://{0}:{1}".format(self.server, self.port),
        #                                  on_message=lambda ws, msg: self.on_message(
        #                                      ws, msg),
        #                                  on_error=lambda ws, err: self.on_error(
        #                                      ws, err),
        #                                  on_close=lambda ws: self.on_close(ws))
        self.ws = websocket.WebSocketApp(self.HOST,
                                         on_message=lambda ws, msg: self.on_message(
                                             ws, msg),
                                         on_error=lambda ws, err: self.on_error(
                                             ws, err),
                                         on_close=lambda ws: self.on_close(ws))
        self.ws.on_open = lambda ws: self.on_open(ws)
        self.ws.run_forever()
        # self.ws = None

    def start(self):
        print("starting the brew service")

        def run(*args):
            self.run()
            rospy.loginfo("calling the run function")
        self.started = True
        self.thread = threading.Thread(target=run)
        self.thread.start()

    def stop(self):
        self.started = False
        if self.ws is not None:
            self.ws.close()
        self.thread.join()


if __name__ == "__main__":
    print("""
This is the Spacebrew module. 
See spacebrew_ex.py for usage examples.
""")

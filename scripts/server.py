#!/usr/bin/env python

from tornado.template import Template
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver

import threading
import json
import os.path

import roslib
import rospy
from std_msgs.msg import String

class Interface():

    callbacks=[]

    def register(self, callback):
        #rospy.loginfo('registering a callback')
        self.callbacks.append(callback)
        
    def unregister(self, callback):
        self.callbacks.remove(callback)

    def notifyInterface(self, msgToInterface):
        for callback in self.callbacks:
            rospy.loginfo('Message sent to Interface')
            callback(msgToInterface)
			

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        index_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), "../web/templates/index.html")
        #loader = tornado.template.Loader(".")
        #self.write(loader.load(index_path).generate())
        self.render(index_path,innerPage="Dream project Setup Interface")

class ModulesInterfaceHandler(tornado.web.RequestHandler):
    def get(self):
        modulesInterface_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), "../web/templates/interfaceTmp.html")
        self.render(modulesInterface_path, page="Modules Interface", modulesInterface="active-link",
                    boxInterface="", buttonsInterface="", actionMapping="", interfaceSrc="modulesInterface", customJS="customModulesInterface")

class BoxInterfaceHandler(tornado.web.RequestHandler):
    def get(self):
        modulesInterface_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), "../web/templates/interfaceTmp.html")
        self.render(modulesInterface_path, page="Box Interface", boxInterface="active-link",
                    modulesInterface="", buttonsInterface="", actionMapping="", interfaceSrc="newboxInterface", customJS="customBoxInterface")
        
class ButtonsInterfaceHandler(tornado.web.RequestHandler):

    def get(self):
        buttonsInterface_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), "../web/templates/interfaceTmp.html")
        self.render(buttonsInterface_path, page="Buttons Interface", buttonsInterface="active-link",
                    boxInterface="", modulesInterface="", actionMapping="", interfaceSrc="buttonsInterface", customJS="customButtonsInterface")

class ActionMappingHandler(tornado.web.RequestHandler):

    def get(self):
        index_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), "..web/templates/index.html")
        loader = tornado.template.Loader(".")
        self.write(loader.load(index_path).generate())


class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        rospy.loginfo("New client !")
        self.application.interface.register(self.upadateInterfaceCallback)
        pass
	
    def on_message(self, message):
        self.write_message(u"Your message was: " + message)
        rospy.loginfo(message)
		
    def on_close(self):
        rospy.loginfo( "Goodbye, connection closed !")
        self.application.interface.unregister(self.upadateInterfaceCallback)
        pass
    
    def check_origin(self, origin):
        return True

    def upadateInterfaceCallback(self, data):
        self.write_message(data)
        

class Application(tornado.web.Application):

    def __init__(self):
        self.interface = Interface()
        handlers = [(r"/", MainHandler),
					(r"/dashboard", MainHandler),
                    (r"/modulesInterface", ModulesInterfaceHandler),
					(r"/buttonsInterface", ButtonsInterfaceHandler),
                    (r"/boxInterface", BoxInterfaceHandler),
					(r"/ws", WebSocketHandler )
        ]

        settings = dict(
            template_path =  os.path.join(os.path.dirname(__file__), "../web/templates"),
            static_path =  os.path.join(os.path.dirname(__file__),"../web/static"),
            debug=True,
        )
        
        tornado.web.Application.__init__(self, handlers, **settings)


class ServerNode():
    def __init__(self, tornadoApp):
        self.application=tornadoApp

    def updateInterfaceCallback(self, data):
        self.application.interface.notifyInterface(data.data)

    def server(self):
        rospy.init_node('server', anonymous=True)
        rospy.loginfo(" Server Node Initialized")
        rospy.Subscriber("modulesInterface", String, self.updateInterfaceCallback)
        rospy.Subscriber("buttonsInterface", String, self.updateInterfaceCallback)
        rospy.Subscriber("boxInterface", String, self.updateInterfaceCallback)
        rospy.spin()


def launchWebserver():    
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    app = Application()
    app.listen(8888)
    serverThread=threading.Thread(target=launchWebserver)
    serverThread.daemon = True
    serverThread.start()
    print " Server Launched on localhost:8888 "
    server_node = ServerNode(app)
    server_node.server()

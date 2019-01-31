import sys
import cv2
import numpy as np
import roslib
import rospy
import argparse
import operator
from std_msgs.msg import String
#from dream_setup_interface.msg import Position, State, Joystick


class VideoCapture:
    def __init__(self, video_source):
        self.video_source = video_source
        if video_source == 'kinectv2':
            self.listener = None
            self.device = None
            self.fn = None
            self.frames = None
            self.startKinectV2Dev()


    def startKinectV2Dev(self):
        from pylibfreenect2 import Freenect2, SyncMultiFrameListener, FrameType

        try:
            from pylibfreenect2 import OpenGLPacketPipeline
            pipeline = OpenGLPacketPipeline()

        except:
            try:
                from pylibfreenect2 import OpenCLPacketPipeline
                pipeline = OpenCLPacketPipeline()

            except:
                from pylibfreenect2 import CpuPacketPipeline
                pipeline = CpuPacketPipeline()
                print("LIBFREENECT2::Packet pipeline:", type(pipeline).__name__)

        self.fn = Freenect2()
        num_devices = self.fn.enumerateDevices()

        if num_devices == 0:
            print("No device connected!")
            sys.exit(1)

        serial = self.fn.getDeviceSerialNumber(0)
        self.device = self.fn.openDevice(serial, pipeline=pipeline)

        self.listener = SyncMultiFrameListener(FrameType.Color)  # listen,ing only to rgb frames

        # Register listeners
        self.device.setColorFrameListener(self.listener)
        self.device.start()

    def stopKinectV2Dev(self):
        self.device.stop()
        self.device.close()

    def stopVideoFeed(self):
        if self.video_source == 'kinectv2':
            self.stopKinectV2Dev()

    def getKinectV1RgbFrame(self):
        import freenect

        array, _ = freenect.sync_get_video()
        rgb_frame = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)

        return rgb_frame

    def getKinectV2RgbFrame(self):
        frames = self.listener.waitForNewFrame()

        return frames

    def getRgbFrame(self):
        rgb_frame = None
        if self.video_source == 'kinectv1':
            import freenect
            rgb_frame = self.getKinectV1RgbFrame()

        elif self.video_source  == 'kinectv2':
            from pylibfreenect2 import Freenect2, SyncMultiFrameListener, FrameType
            rgb_frame = self.getKinectV2RgbFrame()

        return rgb_frame

    def getNextFrame(self):
        print "video source ", self.video_source
        if self.video_source == 'kinectv1':
            rgb_frame = self.getKinectV1RgbFrame()
        elif self.video_source == 'kinectv2':
            if self.frames:
                self.listener.release(self.frames)
            self.frames = self.getKinectV2RgbFrame()
            resised_rgb_frame = cv2.resize(self.frames["color"].asarray(), (int(1920), int(1080)))
            rgb_frame = resised_rgb_frame[:, ::-1, :]
        else:
            print "no video feed"
            return

        frame = cv2.GaussianBlur(rgb_frame, (7, 7), 0)
        return frame

    def launchVideoForColorCalib(self):

        while (1):
            frame = self.getNextFrame()
            # Convert the image to hsv space and find range of colors
            #hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # self.detectReward(frame, hsvFrame)
            # Show the original and processed feed
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            cv2.imshow('Original feed', frame)
            cv2.setMouseCallback('Original feed', self.onMouseClick, hsv_frame)
            # cv2.imshow('Original feed', hsv_frame)

            # if 'q' is pressed then exit the loop
            if cv2.waitKey(33) == ord('q'):
                break

        # Destroy all windows exit the program
        cv2.destroyAllWindows()
        # if self.video_source == 'kinectv2':
        #     self.stopKinectV2Dev()

class InterfaceDetection:
    def __init__(self):
        #self.pub_reward = rospy.Publisher('/activeInterface/reward', Position, queue_size=10)
        self.color_range_dict = {}
        self.video = None
        self.nbr_of_modules = None
        self.selected_pixel = None
        self.interface_detected_area_data = None
        self.current_frame = None

    def setVideoSource(self, video_source):
        self.video = VideoCapture(video_source)

    def onMouseClick(self, event, x, y, flags, params):
        frame = params[0]
        area_type = params[1]
        if event == cv2.EVENT_LBUTTONUP:
            self.selected_pixel =  frame[y, x].tolist()

            # set color
            print "area_type", area_type
            if area_type == "interface":
                self.setInterfaceColorRange(self.selected_pixel)
            elif area_type == "module":
                self.setModulesColorRange(self.selected_pixel)
            else:
                self.setStatusColorRange(self.selected_pixel)
    @staticmethod
    def getColorRangefromHSV(hsv_values):
        lower_bound =  (max(hsv_values[0] - 5, 0), max(hsv_values[1] - 50, 0),  0)
        upper_bound = (min(hsv_values[0] + 5, 180), min(hsv_values[1] + 50, 255), 255)
        return [ np.array(lower_bound), np.array(upper_bound) ]

    def showFrame(self, area_type):
        frame = self.video.getNextFrame()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        cv2.imshow('image', frame)
        cv2.setMouseCallback('image', self.onMouseClick, [hsv_frame, area_type] )
        cv2.waitKey(0)
        cv2.destroyAllWindows()




    def setNbrOfMudules(self, nbr_of_modules):
        self.nbr_of_modules = nbr_of_modules

    def setInterfaceColorRange(self, hsv_values):
        self.color_range_dict["interface"] = self.getColorRangefromHSV(hsv_values)

    def setModulesColorRange(self, hsv_values):
        self.color_range_dict["module"] = self.getColorRangefromHSV(hsv_values)

    def setStatusColorRange(self, hsv_values):
        self.color_range_dict["status"] = self.getColorRangefromHSV(hsv_values)

    def drawBoundingBox(self, frame, label, detected_area_data):
        x, y, w, h = detected_area_data
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, label, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    def drawCenterCercle(self, moment):
        cx, cy = int(moment['m10'] / moment['m00']), int(moment['m01'] / moment['m00'])
        cv2.circle(self.current_frame, (cx, cy), 5, 255, -1)

    def getDetectedObjData(self, detected_area):
        detected_area_data= {"moment": cv2.moments(detected_area),
                             "detected_area_data": cv2.boundingRect(detected_area)}

        return detected_area_data

    def checkCalibration(self):
        if set(['interface', 'module', 'status']).issubset(set(self.color_range_dict.keys())):
            return True
        else:
            return False

    def testDetection(self, area_type):
        self.current_frame = self.video.getNextFrame()
        hsv_frame = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2HSV)
        frame=self.current_frame

        # make sure to run the detection calibration process as follow
        # 1-interface 2-modules 3-status
        if area_type != "interface":
            if area_type == "module":
                if not "interface" in self.color_range_dict.keys() :
                    print "WARNING: Please make sure you to set interface color before"
                    return

            elif area_type == "status":
                if not set(['interface', 'module']).issubset(set(self.color_range_dict.keys())):
                    print "WARNING: Please make sure you to set interface and modules colors  before"
                    return

            x,y,w,h = self.interface_detected_area_data
            print "x ",x,"y ",y,"w ",w,"h ",h
            hsv_frame = hsv_frame[y:y+h,x:x+w]
            frame =frame[y:y+h,x:x+w]

        detected_area = self.locateAreaOfIntrest(frame, hsv_frame, area_type)
        if detected_area["detected"]:
            x, y, w ,h = detected_area["detected_area_data"]
            if area_type == "interface":
                self.interface_detected_area_data = x, y, w ,h

            cv2.imshow('image', self.current_frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print "WARNING: The Best fit for the ", area_type, " is no longer detected :( ..."


    def locateAreaOfIntrest(self, frame, hsv_frame, area_type, area_name=""):

        return_dict = {"detected": False, "detected_area_data": []}

        thresh = cv2.inRange(hsv_frame, self.color_range_dict[area_type.lower()][0],
                             self.color_range_dict[area_type.lower()][1])

        if area_type == "interface":
            black_thresh = cv2.inRange(hsv_frame, np.array((0, 0, 0)),
                              np.array((0, 0, 0)))
            thresh = thresh + black_thresh

        #  Find modules in the filtered image
        _, contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # Compute the coordinates and the dimensions of the biggest area corresponding to the threshold
        max_area = 0
        best_fit = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > max_area:
                max_area = area
                best_fit = cnt

        if best_fit != []:
            return_dict["detected"] = True
            return_dict["detected_area_data"] = self.getDetectedObjData(best_fit)["detected_area_data"]
            self.drawBoundingBox(frame, area_name, return_dict["detected_area_data"])

        return return_dict


    def getModuleInfo(self, frame, hsv_frame, module_name):
        module_info = {"detected": False, "module_data":"", "status_data":""}

        # locate the lever module within the designated area
        module_area_dict = self.locateAreaOfIntrest(frame, hsv_frame, "module", module_name)
        if module_area_dict["detected"]:
            x, y, w ,h = module_area_dict["detected_area_data"]
            hsv_module= hsv_frame[y:y + h, x:x + w]
            rgb_module = frame[y:y + h, x:x + w]

            module_info["module_data"] = x, y, w ,h

            module_status_dict = self.locateAreaOfIntrest(rgb_module, hsv_module, "status")
            if module_status_dict["detected"]:
                module_info["detected"] = True
                module_info["status_data"] = module_status_dict["detected_area_data"]
            else:
                print "WARNING: The ",module_name,"'s status is no longer detected :( ..."
        else:
            print "WARNING: The ",module_name," module is no longer detected :( ..."

        return module_info

    def getRewardState(self, frame, hsv_frame):
        status_dict = {"name": "Reward",  "status": ""}

        reward_info = self.getModuleInfo(frame, hsv_frame,"Reward")
        if reward_info["detected"]:
            x, y, w ,h = reward_info["module_data"]
            x_s, y_s, w_s, h_s = reward_info["status_data"]

            slider_pos = -2 * (y_s * 1.0 + h_s * 1.0 / 2 - h * 1.0 / 2) / (h * 0.9)

            # adjust slider position
            if abs(slider_pos) < 0.01:
                slider_pos = 0
            elif slider_pos > 1:
                slider_pos = 1
            elif slider_pos < -1:
                slider_pos = -1

            status_dict["status"] = "%.2f" % slider_pos
            cv2.putText(frame,status_dict["status"],(x,y+h/2), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,0,0), 1,
                        cv2.LINE_AA)

        return status_dict



class ModulesDetection(InterfaceDetection):

    def __init__(self):
        InterfaceDetection.__init__(self)
        # define modules states publishers
        # self.pub_lever = rospy.Publisher('lever', Position, queue_size=10)
        # self.pub_button = rospy.Publisher('button', State, queue_size=10)
        # self.pub_joystick = rospy.Publisher('joystick', Joystick, queue_size=10)

    def getJoystickState(self, frame, hsv_frame):
        status_dict = {"name": "joystick",  "status": ""}

        joystick_info = self.getModuleInfo(frame, hsv_frame,status_dict["name"])
        if joystick_info["detected"]:
            x, y, w ,h = joystick_info["module_data"]
            x_s, y_s, w_s, h_s = joystick_info["status_data"]

            # Convert Joystick position to oXY frame [-1 1]
            real_x = 2 * (x_s * 1.0 + w_s * 1.0 / 2 - w * 1.0 / 2) / (w * 0.86)
            real_y = 2 * (y_s * 1.0 + h_s * 1.0 / 2 - h * 1.0 / 2) / (h * 0.86)

            # Adjust joystick position
            if abs(real_x) < 0.01:
                real_x = 0
            elif real_x > 1:
                real_x = 1
            elif real_x < -1:
                real_x = -1
            if abs(real_y) < 0.01:
                real_y = 0
            elif real_y > 1:
                real_y = 1
            elif real_y < -1:
                real_y = -1

            status_dict["status"] = "%.1f, %.1f" % (real_x, real_y)
            cv2.putText(frame, status_dict["status"], (x, y + h / 2), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0), 1,
                        cv2.LINE_AA)

        return status_dict

    def getLeverState(self, frame, hsv_frame):
        status_dict = {"name": "lever",  "status": ""}

        lever_info = self.getModuleInfo(frame, hsv_frame,status_dict["name"])
        if lever_info["detected"]:
            x, y, w ,h = lever_info["module_data"]
            x_s, y_s, w_s, h_s = lever_info["status_data"]

            slider_pos= 2*(x_s*1.0+w_s*1.0/2-w*1.0/2)/(w*0.84)

            # adjust slider position
            if abs(slider_pos)<0.01:
                slider_pos = 0
            elif slider_pos>1:
                slider_pos = 1
            elif slider_pos<-1:
                slider_pos = -1

            status_dict["status"] = "%.1f" % slider_pos
            status_dict['state'] = slider_pos

            cv2.putText(frame,status_dict["status"],(x,y+h/2), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,0,0), 1, cv2.LINE_AA)

        return status_dict

    def getButtonState(self, frame, hsv_frame):

        status_dict = {"name": "button",  "status": ""}

        button_info = self.getModuleInfo(frame, hsv_frame, status_dict["name"])
        if button_info["detected"]:
            x, y, w ,h = button_info["module_data"]
            x_s, y_s, w_s, h_s = button_info["status_data"]

            if w_s > w / 2:
                status_dict["status"] = 'OFF'
            else:
                status_dict["status"] = 'ON'

            # show button's state
            cv2.putText(frame, status_dict["status"] , (x + w / 2, y + h / 2), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0), 1,
                        cv2.LINE_AA)

        return status_dict


    def runDetection(self):

        if self.checkCalibration():

            while True:
                self.current_frame = self.video.getNextFrame()
                hsv_frame = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2HSV)

                # detect interface
                interface_area_dict = self.locateAreaOfIntrest(self.current_frame, hsv_frame, "interface", "main Interface")
                if interface_area_dict["detected"]:
                    x, y, w, h = interface_area_dict["detected_area_data"]

                    # define part of the frame where to detect the modules and the reward
                    modules_area = self.current_frame[y:y + h, x:x + 4 * w / 5]
                    reward_area = self.current_frame[y:y + h, x+ 4*w/ 5: x+ w]
                    modules_area_hsv = hsv_frame[y:y + h, x:x + 4 * w / 5]
                    reward_area_hsv = hsv_frame[y:y + h, x+ 4*w/ 5: x+ w]

                    # get button module's status
                    button_status_dict = self.getButtonState(modules_area[h/2:h,w/2:w], modules_area_hsv[h/2:h,w/2:w])

                    # get lever module's status
                    lever_status_dict = self.getLeverState(modules_area[0:h/2,0:w], modules_area_hsv[0:h/2,0:w])

                    # get joystick module's status
                    joystick_status_dict = self.getJoystickState(modules_area[h/2:h,0:w/2], modules_area_hsv[h/2:h,0:w/2])

                    # get reward module's status
                    reward_status_dict = self.getRewardState(reward_area, reward_area_hsv)

                    # Publish module state to the related topics
                    # lever_msg = Position()
                    # lever_msg.name = lever_status_dict["name"]
                    # lever_msg.state = lever_status_dict["state"]
                    # self.pub_lever.publish(lever_msg)
                    #
                    # button_msg = State()
                    # button_msg.name = button_status_dict["name"]
                    # button_msg.state = button_status_dict["state"]
                    # #print(button_msg)
                    # self.pub_button.publish(button_msg)
                    #
                    # joystick_msg = Joystick()
                    # joystick_msg.name = joystick_status_dict["name"]
                    # joystick_msg.position = joystick_status_dict["state"]
                    # self.pub_joystick.publish(joystick_msg)
                    #
                    # reward_msg = Position()
                    # reward_msg.name = reward_status_dict["name"]
                    # reward_msg.state = reward_status_dict["state"]
                    # #print(reward_msg)
                    # self.pub_reward.publish(reward_msg)

                else:
                    print "WARNING: The Best fit for the interface is no longer detected :( ..."

                cv2.imshow('Original feed', self.current_frame)
                #cv2.imshow('Original feed', hsv_frame)

                # if 'q' is pressed then exit the loop
                if cv2.waitKey(33) == ord('q'):
                    break

            # Destroy all windows exit the program
            cv2.destroyAllWindows()
            self.video.stopVideoFeed()
        else:
            print "WARNING: Please make sur to select areas to be detected."

class ButtonsDetection(InterfaceDetection):

    def __init__(self):
        InterfaceDetection.__init__(self)
        # self.pub_green_button = rospy.Publisher('button', State, queue_size=10)
        # self.pub_square_green_button = rospy.Publisher('button', State, queue_size=10)
        # self.pub_red_button = rospy.Publisher('button', State, queue_size=10)
        # self.pub_yellow_button = rospy.Publisher('button', State, queue_size=10)
        # self.pub_blue_button = rospy.Publisher('button', State, queue_size=10)

class BoxDetection(InterfaceDetection):

    def __init__(self):
        InterfaceDetection.__init__(self)
        #self.pub_box = rospy.Publisher('button', State, queue_size=10)



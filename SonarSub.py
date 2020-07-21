#!/usr/bin/python

import rospy
from std_msgs.msg import Float32MultiArray
from adafruit_servokit import ServoKit
import Jetson.GPIO as GPIO
import time


kit = ServoKit(channels=16)

def callback(data):
	#a = Float32MultiArray()
	print (data.data[0], data.data[1])
	#while not rospy.is_shutdown():

		#try:
	kit.servo[0].angle = data.data[0]
	kit.continuous_servo[1].throttle = data.data[1]
	
		#except rospy.ROSInterruptException:
			#pass


def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("chatter", Float32MultiArray, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()


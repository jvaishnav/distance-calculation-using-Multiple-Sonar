#!/usr/bin/python

import rospy
import Jetson.GPIO as GPIO
import time
import math
import logging

from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import Bool

GPIO.setmode(GPIO.BOARD)
# Define GPIO for Central Sensor
Echo_Cen_IP =13
Trig_Cen_OP =23
# Define GPIO for Left Sensor
Echo_Lt_IP =38
Trig_Lt_OP =40
# Define GPIO for Right Sensor
Echo_Rt_IP =21
Trig_Rt_OP =24

GPIO.setup([Trig_Cen_OP, Trig_Lt_OP, Trig_Rt_OP],GPIO.OUT, initial=GPIO.LOW)  # Trigger > Out
GPIO.setup([Echo_Cen_IP,Echo_Lt_IP,Echo_Rt_IP], GPIO.IN)    # Echo < In

global Ang_Thro
Ang_Thro = Float32MultiArray()
Ang_Thro.data = [0, 0]



# Obstacle distance Calculation
def obstacle_dis(Trig_OP, Echo_IP):
    GPIO.output(Trig_OP, GPIO.HIGH)
    time.sleep(0.00001)
    #  Set trigger to Low - 0
    GPIO.output(Trig_OP, GPIO.LOW)
    # Check for the Echo pulse and get the Start and End Time stamps
    Start = 0
    Stop = 0
    while GPIO.input(Echo_IP) != 1:
    	Start = time.time()
    while GPIO.input(Echo_IP) != 0:
       	Stop = time.time()
    # Calculate pulse length
    Tot_Time = Stop - Start
    # Distance pulse travelled = (Total time *  speed of sound )/2 (cm/s)
    distance = int(Tot_Time * 17150)  # distance in one direction
    #print ("Distance =", distance)
    return distance

# Driving Function - Throttle - Angle specified
def goforward():
    Ang_Thro.data = [88,0.24]
def turn_left():
    Ang_Thro.data = [45,0.24]
def turn_right():
    Ang_Thro.data = [135,0.24]
#def gobackward():
#    Ang_Thro.data = [80,-0.22]
def stop_1():
    Ang_Thro.data = [80, 0.0]

# Obstacle distance from Front, Right and Left sensors
def front_obstacle():
    return (obstacle_dis(Trig_Cen_OP,Echo_Cen_IP))
def right_obstacle():
    return(obstacle_dis(Trig_Rt_OP,Echo_Rt_IP))
def left_obstacle():
    return(obstacle_dis(Trig_Lt_OP,Echo_Lt_IP))


def Drive():

	while not rospy.is_shutdown():
		# Sense the front obstacle
		fr_obs_dis = front_obstacle()
		rt_obs_dis = right_obstacle()
		lt_obs_dis = left_obstacle()
		print ("Center sensor = ", fr_obs_dis)
		print ("Right sensor = ", rt_obs_dis)
		print ("Left sensor = ", lt_obs_dis)

		if (fr_obs_dis <= 60 and rt_obs_dis <= 60 and rt_obs_dis <= 60):
			stop_1()
		elif (fr_obs_dis <= 60 and rt_obs_dis > lt_obs_dis): 
			turn_right()
		elif (fr_obs_dis <= 60 and rt_obs_dis < lt_obs_dis): 
			turn_left()	
		else:
			goforward()
		print(Ang_Thro)
		pub = rospy.Publisher('chatter', Float32MultiArray, queue_size=10)
		rospy.init_node('Drive', anonymous=True)
	
		rospy.loginfo(Ang_Thro)
		pub.publish(Ang_Thro)


if __name__ == '__main__':
    try:
        Drive()
    except rospy.ROSInterruptException:
        pass

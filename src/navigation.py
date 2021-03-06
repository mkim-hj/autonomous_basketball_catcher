#! /usr/bin/env python

import rospy
import tf
from os import system
from geometry_msgs.msg import Point
from std_msgs.msg import String
from math import atan2, sqrt, pi

class Navigation:

	def __init__(self):
		rospy.init_node('navigation')
		listener = tf.TransformListener()
		self.control_state = 'waiting'
		# rospy.Subscriber('/catcher/control', String, self.received_control)
		while not rospy.is_shutdown():
			try:
				raw_input()
				now = rospy.Time.now()
				listener.waitForTransform('robot', 'trash', now, rospy.Duration(2.0))
				position, orientation = listener.lookupTransform('robot', 'trash', now)
				self.send(position[0], position[1])
			except tf.Exception as e:
				rospy.logerr(e)

	def send(self, x, y):
		x, y = 32768 + int(x * 1000), 32768 + int(y * 1000)
		system('gatttool -b CC:B1:07:3E:1B:F9 -t random --char-write --handle=0xb --value=%0.4x%0.4x'%(x, y))

	def received_control(self, msg):
		self.control_state = msg.data

if __name__ == '__main__':
	Navigation()
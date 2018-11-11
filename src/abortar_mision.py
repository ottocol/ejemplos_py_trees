#!/usr/bin/env python
import rospy
from std_msgs.msg import Bool

def talker():
    pub = rospy.Publisher('abortar_mision', Bool, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    pub.publish(True)

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
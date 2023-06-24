#!/usr/bin/env python

import rospy
from geometry_msgs.msg import TwistStamped
from magang.srv import pidFeedback

def initiate_pid(feddback):
    rospy.wait_for_service('Set_Feedback')
    try:
        pid_req = rospy.ServiceProxy('Set_Feedback', pidFeedback)
        response = pid_req(feddback)
        return response.newResult
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

if __name__ == "__main__":
    rate = rospy.Rate(0.1)
    while True:
        rospy.Subscriber('mavros/global_position/velocity', TwistStamped, initiate_pid)
        rate.sleep()

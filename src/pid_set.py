#!/usr/bin/env python

import sys
import rospy
from magang.srv import pidSet, pidInitiate

def initiate_pid(p, i, d, set):
    rospy.wait_for_service('Initiate_PID')
    try:
        pid_req = rospy.ServiceProxy('Initiate_PID', pidInitiate)
        response = pid_req(p, i, d, set)
        return response.result
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def set_pid(p, i, d):
    rospy.wait_for_service('Set_PID_Value')
    try:
        pid_req = rospy.ServiceProxy('Set_PID_Value', pidSet)
        response = pid_req(p, i, d)
        return response.nResult
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def usage():
    return "%s [P I D Target] atau [P I D]"%sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 5:    
        w = float(sys.argv[1])
        x = float(sys.argv[2])
        y = float(sys.argv[3])
        z = float(sys.argv[4])

        initiate_pid(w, x, y, z)
        print(f'P: {w}, I: {x}, D: {y}, Target: {z}')

    elif len(sys.argv) == 4:
        a = float(sys.argv[1])
        b = float(sys.argv[2])
        c = float(sys.argv[3])

        set_pid(a, b, c)
        print(f'P: {a}, I: {b}, D: {c}')

    else:
        print(usage())
        sys.exit(1)

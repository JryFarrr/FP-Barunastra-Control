#!/usr/bin/env python

from magang.srv import pidInitiate, pidInitiateResponse
from magang.srv import pidSet, pidSetResponse
from magang.srv import pidFeedback, pidFeedbackResponse
from magang.msg import truster
import rospy

class PID:
    def __init__(self, P, I, D, Target):
        self.__p = P
        self.__i = I
        self.__d = D
        self.__target = Target
        self.__feedback = 0 
        self.__last_err = 0

        self.__max_i = 1000

        self.__max_out = 1000
        self.__min_out = 0

        self.__cur_err = 0
        self.__integral_cum = 0 
        self.__cycle_derivative = 0 



    def calculation(self):
        self.__cur_err = self.__target - self.__feedback
        self.__integral_cum += self.__cur_err
        self.__cycle_derivative = self.__cur_err - self.__last_err
 
        if self.__integral_cum > self.__max_i:
            self.__integral_cum = self.__max_i
        elif self.__integral_cum < -self.__max_i:
            self.__integral_cum = -self.__max_i
        
        output = (self.__cur_err * self.__p) + (self.__integral_cum * self.__i) + (self.__cycle_derivative * self.__d)
        if output > self.__max_out:
            output = self.__max_out
        elif output < self.__min_out:
            output = self.__min_out

        self.__last_err = self.__cur_err
        
        return output
    
    def initiate(self, kp, ki, kd, set_point):
        self.__p = kp
        self.__i = ki
        self.__d = kd
        self.__target = set_point

    def set(self, P, I, D):
        self.__p = P
        self.__i = I
        self.__d = D
    
    def feedback(self, input):
        self.__feedback = input

pid = PID(0, 0, 0, 0)

def initiate_pid(req):
    pid.initiate(req.kp, req.ki, req.kd, req.target)
    output = truster()
    output.vel = pid.calculation()
    output.pesan = 'PID result:'
    print(f'{output.pesan} {output.vel}')

    response = pidInitiateResponse()
    response.result = output.vel

    return response

def set_pid(req):

    pid.set(req.nP, req.nI, req.nD)
    output = truster()
    output.vel = pid.calculation()
    output.pesan = 'PID result: '
    print(f'{output.pesan} {output.vel}')

    response = pidSetResponse()
    response.nResult = output

    return response    

def set_feedback(req):
    pid.feedback(req.setF)
    output = truster()
    output.pesan = 'PID result: '
    output.vel = pid.calculation()
    print(f'{output.pesan} {output.vel}')

    response = pidFeedbackResponse()
    response.newResult = output

    return response    

def main_server():
    rospy.init_node('PID_service')
    rospy.Service('Initiate_PID', pidInitiate, initiate_pid)
    rospy.Service('Set_PID_Value', pidSet, set_pid)
    rospy.Service('Set_Feedback', pidFeedback, set_feedback)
    print("Ready to set PID.")
    rospy.spin()

if __name__ == "__main__":
    main_server()
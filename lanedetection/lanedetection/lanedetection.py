#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rclpy, cv2
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
import numpy as np
from std_msgs.msg import Bool
import time
from ai_msgs.msg import PerceptionTargets
        
class LaneDetection(Node):
    def __init__(self):
        super().__init__('lanedetection')
        self.get_logger().info("Start lane keeping.")
        print("Start")

        self.pct_sub = self.create_subscription(Twist, '/pct_vel', 
            self.pct_callback, 10)
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.obs_sub = self.create_subscription(Bool, '/has_obs',self.obs_callback,10)
        self.redl=False
        self.traffic_sub= self.create_subscription(PerceptionTargets, "/traffice_sign", self.traffic_callback, 10) 
        self.twist = Twist()   
        self.pct = Twist() 
        self.has_obs = False

    def on_shutdown(self):
        self.twist.linear.x = 0.0
        self.twist.angular.z = 0.0 
        self.cmd_vel_pub.publish(self.twist) 

    def obs_callback(self, msg):
        self.has_obs = msg.data
    def traffic_callback(self, msg): 
        self.redl=False
        for boxes in msg.targets:
            #self.redl=False
            if boxes.rois[0].confidence > 0.5 and boxes.rois[0].type == 'red_light':                
                print('red_light')       
                self.redl=True
                time.sleep(3)
            elif boxes.rois[0].confidence > 0.5 and boxes.rois[0].type == 'green_light\r':
                print('green_light')       
                self.redl=False
    def pct_callback(self, msg):
        #print('循环执行中')
        #print(self.has_obs)
        print(self.redl)
        if self.redl==True:
            print("Stop!")
            self.twist.linear.x=0.0
            self.twist.angular.z=0.0
        elif self.has_obs: 
            print("Detected!")
            self.twist.linear.x=0.0
            self.twist.angular.z=6.4
            time.sleep(1)
        
        else: 
  
          
          self.pct=msg
          #self.pct.linear.x  推理出来的小车车速
          #self.pct.angular.z 推理出来的小车转角

          self.twist.linear.x =1.3*0.32    #控制小车速度
          self.twist.angular.z =2.6*self.pct.angular.z     #控制小车转角             
                   
        
        self.cmd_vel_pub.publish(self.twist)   
       
        
     
def main(args=None):
    rclpy.init(args=args)      
    lanedetection = LaneDetection()
    try:
        rclpy.spin(lanedetection)
    except KeyboardInterrupt:
        lanedetection.on_shutdown()
        lanedetection.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

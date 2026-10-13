#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rclpy, cv2
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
import datetime 
import os
import numpy as np
import sys, select, tty, termios
from cv_bridge import CvBridge

class Picker(Node):
    def __init__(self):
        super().__init__('picture_recorder')
        self.get_logger().info("start picking picture!")
        self.n = 0
        self.image_sub = self.create_subscription(CompressedImage, '/image', self.image_callback, 10)
    
    def get_key(self,settings):    
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key


    def image_callback(self, msg):
        settings = None
        settings = termios.tcgetattr(sys.stdin)
        key = self.get_key(settings)        
        if key=='\r':
            print("record %d picturs"%self.n)
            pick_string = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S_%f') 
            img_name = pick_string+'.jpg'
            img_save_path = os.path.join('/userdata/pictures/img', img_name)            
            self.image = CvBridge().compressed_imgmsg_to_cv2(msg)
            cv2.imwrite(img_save_path, self.image)    
            self.n+=1 
        
   
def main(args=None):
    rclpy.init(args=args)    
    picker = Picker()
    try:
        rclpy.spin(picker)
    except KeyboardInterrupt:    	
        print('ctr+C')
    finally:  
        picker.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
